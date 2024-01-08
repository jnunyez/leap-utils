# utility for creating a leap-seconds.list file

import datetime as dt
import pytz
import hashlib as sha

NTP_EPOCH = dt.datetime(1900, 1, 1, 0, 0, 0, tzinfo=pytz.utc)


def ntp_timestamp(date):
    # NTP leap-seconds.list wants seconds since 1900
    return int((date - NTP_EPOCH).total_seconds())


# when was the file updated with a new leap second value?
update = dt.datetime(2016, 7, 8, tzinfo=pytz.utc)

# the leap-seconds
# TODO: use ubxtool to get the leapseconds if needed
leap_seconds = [
    dt.datetime(1972, 1, 1, tzinfo=pytz.utc),
    dt.datetime(1972, 7, 1, tzinfo=pytz.utc),
    dt.datetime(1973, 1, 1, tzinfo=pytz.utc),
    dt.datetime(1974, 1, 1, tzinfo=pytz.utc),
    dt.datetime(1975, 1, 1, tzinfo=pytz.utc),
    dt.datetime(1976, 1, 1, tzinfo=pytz.utc),
    dt.datetime(1977, 1, 1, tzinfo=pytz.utc),
    dt.datetime(1978, 1, 1, tzinfo=pytz.utc),
    dt.datetime(1979, 1, 1, tzinfo=pytz.utc),
    dt.datetime(1980, 1, 1, tzinfo=pytz.utc),
    dt.datetime(1981, 7, 1, tzinfo=pytz.utc),
    dt.datetime(1982, 7, 1, tzinfo=pytz.utc),
    dt.datetime(1983, 7, 1, tzinfo=pytz.utc),
    dt.datetime(1985, 7, 1, tzinfo=pytz.utc),
    dt.datetime(1988, 1, 1, tzinfo=pytz.utc),
    dt.datetime(1990, 1, 1, tzinfo=pytz.utc),
    dt.datetime(1991, 1, 1, tzinfo=pytz.utc),
    dt.datetime(1992, 7, 1, tzinfo=pytz.utc),
    dt.datetime(1993, 7, 1, tzinfo=pytz.utc),
    dt.datetime(1994, 7, 1, tzinfo=pytz.utc),
    dt.datetime(1996, 1, 1, tzinfo=pytz.utc),
    dt.datetime(1997, 7, 1, tzinfo=pytz.utc),
    dt.datetime(1999, 1, 1, tzinfo=pytz.utc),
    dt.datetime(2006, 1, 1, tzinfo=pytz.utc),
    dt.datetime(2009, 1, 1, tzinfo=pytz.utc),
    dt.datetime(2012, 7, 1, tzinfo=pytz.utc),
    dt.datetime(2015, 7, 1, tzinfo=pytz.utc),
    dt.datetime(2017, 1, 1, tzinfo=pytz.utc),
]

# when does the file expire?
# use ubxtool to get the date of when this file will expire
expires = dt.datetime(2024, 6, 28, tzinfo=pytz.utc)


TEMPLATE = """# generated on {now}
# this program/generator available from:
# https://github.com/jnunyez/leap-utils
#
# updated {update}
#$\t{update_timestamp}
#
# expires {expires}
#@\t{expires_timestamp}
#
# Leap seconds
{leap_seconds}
#
# SHA1 hash for this file:
#h\t{hash}
# end of file.
"""


def write_leap_seconds_file(fname, leap_seconds, update, expires, ls_offset):
    s = sha.new("sha1")
    s.update(str(ntp_timestamp(update)).encode("utf-8"))
    s.update(str(ntp_timestamp(expires)).encode("utf-8"))

    formatted_leap_seconds = []
    for ls, d in enumerate(leap_seconds, ls_offset):
        #print(ls)
        #print(d)
        ntp_t = ntp_timestamp(d)
        formatted_leap_seconds.append(f"{ntp_t}\t{ls}\t# {d.strftime('%Y-%m-%d')}")
        s.update(str(ntp_t).encode("utf-8"))
        s.update(str(ls).encode("utf-8"))

    sha1 = s.hexdigest()
    shaSplit = [
        sha1[0:8],
        sha1[8:16],
        sha1[16:24],
        sha1[24:32],
        sha1[32:40],
    ]

    with open(fname, "w") as f:
        f.write(
            TEMPLATE.format(
                now=dt.datetime.now(),
                update=update,
                update_timestamp=ntp_timestamp(update),
                expires=expires,
                expires_timestamp=ntp_timestamp(expires),
                leap_seconds="\n".join(formatted_leap_seconds),
                hash=" ".join(shaSplit),
            )
        )

if __name__ == "__main__":
    write_leap_seconds_file("my-leap-seconds.list", leap_seconds, update, expires, 10)
