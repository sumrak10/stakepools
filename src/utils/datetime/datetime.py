import datetime


def get_current_utc_datetime(
        *,
        sub: datetime.timedelta | None = None,
        add: datetime.timedelta | None = None,
        relpace_tz_info: bool = True
) -> datetime.datetime:
    now = datetime.datetime.now(datetime.timezone.utc).replace(
        tzinfo=None if relpace_tz_info else datetime.timezone.utc)
    if sub is not None:
        now -= sub
    if add is not None:
        now += add
    return now

