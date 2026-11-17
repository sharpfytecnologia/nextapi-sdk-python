"""Contrato compartilhado pelos seis SDKs (sdks/contract/cases.json).

Os casos usam os nomes canônicos (camelCase); aqui viram os nomes do Python (snake_case), nos métodos e nos
parâmetros nomeados.
"""
import json
import re
import unittest
from pathlib import Path
from unittest import mock
from urllib.parse import parse_qsl, urlsplit

import sharpfy_nextapi.client as client_module
from sharpfy_nextapi import (NextApiAuthenticationError, NextApiClient, NextApiConnectionError,
                             NextApiInsufficientCreditsError, NextApiNotFoundError, NextApiPaidPlanRequiredError,
                             NextApiRateLimitError, NextApiServerError, NextApiValidationError, normalize_cnpj)
from sharpfy_nextapi._transport import Response

# Contrato em sdks/contract (monorepo) ou em contract/ dentro do SDK (espelho público).
CONTRACT_DIR = next(d for d in (Path(__file__).resolve().parents[1] / "contract", Path(__file__).resolve().parents[2] / "contract") if d.is_dir())
CONTRACT = json.loads((CONTRACT_DIR / "cases.json").read_text("utf-8"))
KEY = "nxa_test_0123456789abcdef"


def snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


class FakeTransport:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, method, url, headers, body, timeout):
        self.calls.append({"method": method, "url": url, "headers": headers, "body": body})
        item = self.responses.pop(0) if len(self.responses) > 1 else self.responses[0]
        if isinstance(item, Exception):
            raise item
        return item


def ok(body, status=200, headers=None):
    return Response(status, headers or {}, json.dumps(body).encode("utf-8"))


def client(transport, **kwargs):
    kwargs.setdefault("max_retries", 2)
    return NextApiClient(KEY, transport=transport, **kwargs)


def invoke(api, call, args):
    resource, method = call.split(".")
    target = getattr(getattr(api, resource), snake(method))
    positional = list(args)
    options = positional.pop() if positional and isinstance(positional[-1], dict) else {}
    return target(*positional, **{snake(k): v for k, v in options.items()})


ERRORS = {
    "authentication": NextApiAuthenticationError,
    "insufficientCredits": NextApiInsufficientCreditsError,
    "paidPlanRequired": NextApiPaidPlanRequiredError,
    "notFound": NextApiNotFoundError,
    "validation": NextApiValidationError,
    "rateLimit": NextApiRateLimitError,
    "server": NextApiServerError,
}


@mock.patch.object(client_module.time, "sleep", lambda _: None)
class ContractTests(unittest.TestCase):
    def test_cases(self):
        for case in CONTRACT["cases"]:
            with self.subTest(case["id"]):
                transport = FakeTransport(ok(case["response"]))
                result = invoke(client(transport), case.get("call", case["id"]), case["args"])
                self.assertEqual(len(transport.calls), 1)
                call = transport.calls[0]
                url = urlsplit(call["url"])
                self.assertEqual(call["method"], case["method"])
                self.assertEqual(f"{url.scheme}://{url.netloc}", "https://api.nextapi.com.br")
                self.assertEqual(url.path, case["path"])
                self.assertEqual(dict(parse_qsl(url.query)), case["query"])
                self.assertEqual(call["headers"]["Authorization"], f"Bearer {KEY}")
                self.assertRegex(call["headers"]["User-Agent"], r"^nextapi-python/\d+\.\d+\.\d+ python/")
                self.assertRegex(call["headers"]["X-NextApi-Client"], CONTRACT["headers"]["client"])
                self.assertRegex(call["headers"]["X-NextApi-Client-Info"], CONTRACT["headers"]["info"])
                if "body" in case:
                    self.assertEqual(call["headers"]["Content-Type"], "application/json")
                    self.assertEqual(json.loads(call["body"]), case["body"])
                else:
                    self.assertIsNone(call["body"])
                self.assertEqual(result, case["response"])

    def test_app_info_is_sanitized(self):
        spec = CONTRACT["headers"]["appInfo"]
        transport = FakeTransport(ok({}))
        client(transport, app_info=spec["input"]).creditos.consultar()
        headers = transport.calls[0]["headers"]
        self.assertTrue(headers["User-Agent"].endswith(" " + spec["sanitized"]))
        self.assertTrue(headers["X-NextApi-Client-Info"].endswith("; " + spec["sanitized"]))
        self.assertRegex(headers["X-NextApi-Client-Info"], CONTRACT["headers"]["info"])

    def test_invalid_input_never_reaches_the_api(self):
        for case in CONTRACT["invalid"]:
            with self.subTest(case["reason"]):
                transport = FakeTransport(ok({}))
                with self.assertRaises(NextApiValidationError):
                    invoke(client(transport), case["call"], case["args"])
                self.assertEqual(transport.calls, [])

    def test_valid_inputs(self):
        for case in CONTRACT["valid"]:
            transport = FakeTransport(ok({}))
            invoke(client(transport), case["call"], case["args"])
            self.assertEqual(urlsplit(transport.calls[0]["url"]).path, case["path"])

    def test_errors(self):
        for case in CONTRACT["errors"]:
            with self.subTest(f"{case['status']}/{case['body']['code']}"):
                transport = FakeTransport(ok(case["body"], case["status"], {"x-request-id": "req-1", "retry-after": "0"}))
                with self.assertRaises(ERRORS[case["error"]]) as raised:
                    client(transport).cnpj.consultar("11222333000181")
                error = raised.exception
                self.assertEqual(error.status, case["status"])
                self.assertEqual(error.code, case["body"]["code"])
                self.assertEqual(error.message, case["body"]["message"])
                self.assertEqual(error.request_id, "req-1")
                self.assertEqual(len(transport.calls), 3 if case.get("retryable") else 1)


@mock.patch.object(client_module.time, "sleep", lambda _: None)
class BehaviourTests(unittest.TestCase):
    def test_retry_then_success(self):
        transport = FakeTransport(ok({}, 503, {"retry-after": "0"}), ok({"cnpj": "1"}))
        self.assertEqual(client(transport).cnpj.consultar("11222333000181"), {"cnpj": "1"})
        self.assertEqual(len(transport.calls), 2)

    def test_batch_post_is_never_retried(self):
        transport = FakeTransport(ok({"code": 1014, "message": "x"}, 503))
        with self.assertRaises(NextApiServerError):
            client(transport).cnpj.consultar_lote(["11222333000181"])
        self.assertEqual(len(transport.calls), 1)

    def test_network_error_retried_then_connection_error_without_key(self):
        transport = FakeTransport(OSError("connection refused"))
        with self.assertRaises(NextApiConnectionError) as raised:
            client(transport, max_retries=1).creditos.consultar()
        self.assertEqual(len(transport.calls), 2)
        self.assertNotIn(KEY, str(raised.exception))

    def test_redirect_is_an_error(self):
        transport = FakeTransport(Response(302, {"location": "https://evil.example/"}, b""))
        with self.assertRaises(NextApiConnectionError):
            client(transport).creditos.consultar()
        self.assertEqual(len(transport.calls), 1)

    def test_non_json_error_body(self):
        transport = FakeTransport(Response(500, {}, b"<html>Bad Gateway</html>"))
        with self.assertRaises(NextApiServerError) as raised:
            client(transport, max_retries=0).creditos.consultar()
        self.assertEqual(raised.exception.message, "HTTP 500")
        self.assertEqual(raised.exception.body, "<html>Bad Gateway</html>")

    def test_key_is_not_shown(self):
        api = client(FakeTransport(ok({})))
        self.assertNotIn(KEY, repr(api))
        self.assertNotIn(KEY, str(api))
        self.assertEqual(api.environment, "sandbox")

    def test_base_url_requires_https(self):
        with self.assertRaises(ValueError):
            NextApiClient(KEY, base_url="http://api.nextapi.com.br")
        NextApiClient(KEY, base_url="http://localhost:5112")

    def test_key_from_environment(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(NextApiAuthenticationError):
                NextApiClient()
        with mock.patch.dict("os.environ", {"NEXTAPI_KEY": "nxa_live_abc"}):
            self.assertEqual(NextApiClient().environment, "production")

    def test_alphanumeric_cnpj(self):
        self.assertEqual(normalize_cnpj("12.abc.345/01de-35"), "12ABC34501DE35")

    def test_real_transport_refuses_redirects(self):
        """O transporte padrão (urllib) não segue redirecionamento: sem isso a chave iria para outro host."""
        import http.server
        import threading
        from sharpfy_nextapi._transport import UrllibTransport

        seen = []

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                seen.append(self.path)
                self.send_response(302)
                self.send_header("Location", "/outro")
                self.end_headers()

            def log_message(self, *args):
                pass

        server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            api = NextApiClient(KEY, base_url=f"http://localhost:{server.server_port}", transport=UrllibTransport())
            with self.assertRaises(NextApiConnectionError):
                api.creditos.consultar()
            self.assertEqual(seen, ["/v1/credits"])
        finally:
            server.shutdown()
            server.server_close()



SMOKE_KEY = __import__("os").environ.get("NEXTAPI_SMOKE_KEY")
SMOKE_ENV = __import__("os").environ.get("NEXTAPI_SMOKE_ENV", "production")


@unittest.skipUnless(SMOKE_KEY, "fumaça: defina NEXTAPI_SMOKE_KEY (sdks/smoke.sh)")
class SmokeTests(unittest.TestCase):
    """Fumaça contra a API publicada, com o transporte real."""

    def test_smoke(self):
        steps = json.loads((CONTRACT_DIR / "smoke.json").read_text("utf-8"))["steps"]
        for step in steps:
            if step.get("env") not in (None, SMOKE_ENV):
                continue
            with self.subTest(step["id"]):
                key = SMOKE_KEY[:9] + "chave-invalida" if step.get("badKey") else SMOKE_KEY
                api = NextApiClient(key, max_retries=4)
                got, detail = "ok", ""
                try:
                    invoke(api, step["call"], step["args"])
                except NextApiConnectionError as e:
                    got, detail = "connection", f" ({e.message})"
                except Exception as e:  # noqa: BLE001
                    got = next((k for k, v in ERRORS.items() if isinstance(e, v)), "other")
                    detail = f" ({getattr(e, 'status', '')}/{getattr(e, 'code', '')} {e} req={getattr(e, 'request_id', None)})"
                print(f"SMOKE python {SMOKE_ENV} {step['id']}: {got}{detail}", flush=True)
                self.assertIn(got, step["expect"])


if __name__ == "__main__":
    unittest.main()
