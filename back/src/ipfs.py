# Standard library
import asyncio
from contextlib import (
    asynccontextmanager,
)
import json
from typing import (
    Dict,
    Tuple,
)

# Local libraries
import config.cachipfs
from logs import (
    log,
)
import system


def get_env() -> Dict[str, str]:
    return {
        'IPFS_PATH': config.cachipfs.IPFS_REPO,
    }


async def _raise(
    code: int,
    command: Tuple[str, ...],
    err: bytes,
    out: bytes,
) -> None:
    await log(
        'error',
        'Command: %s\n'
        'Exit code: %s\n'
        'Stdout: %s\n'
        'Stderr: %s\n',
        command,
        code,
        out.decode(),
        err.decode(),
    )

    raise SystemError()


async def add(path: str) -> str:
    command: Tuple[str, ...] = (
        'ipfs',
        'add',
        '--chunker', 'size-1024',
        '--hash', 'sha2-256',
        '--quieter',
        '--pin',
        path,
    )

    code, out, err = await system.read(*command, env=get_env())
    cid = out.decode()

    if code == 0:
        await log('info', 'IPFS added cid: %s', cid)
    else:
        await _raise(code=code, command=command, err=err, out=out)

    return cid


async def is_available(cid: str, *, timeout: str = '5s') -> bool:
    command: Tuple[str, ...] = (
        'ipfs',
        '--timeout', timeout,
        'cat',
        '--length', '1',
        cid,
    )

    code, *_ = await system.read(*command, env=get_env())

    return code == 0


@asynccontextmanager
async def get(cid: str, *, timeout: str = '60s') -> str:
    async with config.ephemeral_file() as path:
        command: Tuple[str, ...] = (
            'ipfs',
            '--timeout', timeout,
            'get',
            '--output', path,
            cid,
        )

        code, out, err = await system.read(*command, env=get_env())

        if code == 0:
            await log('info', 'IPFS got cid: %s', cid)
        else:
            await _raise(code=code, command=command, err=err, out=out)

        yield path