import base58

USDT_CONTRACT_ADDRESS = "TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs"  #"TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
TOKENS_DECIMALS = {
    USDT_CONTRACT_ADDRESS: 6,
}


def hex_to_base58(hex_address: str) -> str | None:
    """Конвертирует hex-адрес (с префиксом 41) в Base58Check (TX..., TN...)"""
    if not hex_address.startswith("41") or len(hex_address) != 42:
        return None
    address_bytes = bytes.fromhex(hex_address)
    checksum = address_bytes[:21]  # Первые 21 байт
    return base58.b58encode_check(checksum).decode()


def generate_memo(user_id: int, pool_id: int) -> str:
    return str(user_id) + "__" + str(pool_id)


def parse_memo(memo: str) -> tuple[int, int]:
    user_id, pool_id = memo.split("__")
    return int(user_id), int(pool_id)