"""CS-030 — Spike sintético de projeção/publicação (Phase 1).

Módulo local-only que aceita somente fixtures sintéticas. Não tem descoberta de
filesystem, rede, integração de vault, secret store nem identidade de produção.

Usado pelos testes em tests/test_cs030_synthetic_spike.py para validar:
- Filtro positivo (somente registros allowlisted/scope)
- Negação de identidade sintética desconhecida
- Write-deny (reader não pode escrever/mutar a publicação)
- Revogação fail-closed sem mutar registros publicados
- Integridade (publicação adulterada falha)
- Projeção somente de canônicos vigentes no scope permitido
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any


def _digest(records: dict[str, dict[str, Any]]) -> str:
    payload = json.dumps(records, sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


@dataclass
class SyntheticPublication:
    records: dict[str, dict[str, Any]]
    digest: str
    revoked: bool = False


class SyntheticProjectionPublisher:
    """Materialize a positive-list projection from synthetic fixture records."""

    def __init__(self, *, allowed_scope: str, allowed_audience: str) -> None:
        self.allowed_scope = allowed_scope
        self.allowed_audience = allowed_audience

    def publish(self, records: list[dict[str, Any]]) -> SyntheticPublication:
        eligible = {
            record["id"]: deepcopy(record)
            for record in records
            if record["status"] == "canonical"
            and record["scope"] == self.allowed_scope
            and record["audience"] == self.allowed_audience
            and record["sensitivity"] in {"public", "internal"}
            and record["expires_at"] is None
        }
        return SyntheticPublication(records=eligible, digest=_digest(eligible))

    def revoke(self, publication: SyntheticPublication) -> None:
        publication.revoked = True


class SyntheticVPSReader:
    """Read-only synthetic consumer; no source or credential surface exists."""

    def __init__(self, publication: SyntheticPublication, *, identity: str) -> None:
        self._publication = publication
        self._identity = identity

    def retrieve(self, record_id: str) -> dict[str, Any] | None:
        if (
            self._identity != "synthetic-vps"
            or self._publication.revoked
            or _digest(self._publication.records) != self._publication.digest
        ):
            return None
        record = self._publication.records.get(record_id)
        return deepcopy(record) if record else None

    def write(self, record_id: str, record: dict[str, Any]) -> None:
        raise PermissionError("synthetic VPS reader is read-only")
