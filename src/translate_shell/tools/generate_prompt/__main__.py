r"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.

generate prompt by `translate_shell.utils.misc`'s `p10k_sections()`.
By default, it is for `lftp <https://lftp.yar.ru/>`_.
See section ``cmd:prompt`` of `man lftp <https://lftp.yar.ru/lftp-man.html>`_.
::
    install -d ~/.config/lftp/lftp
    python -m translate_shell.tools.generate_prompt > ~/.config/lftp/lftp/rc
    echo 'source ~/.config/lftp/lftp/rc' >> ~/.config/lftp/rc
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime

from ... import __name__ as NAME
from ... import __version__

try:
    import shtab
except ImportError:
    from ...external import shtab

NAME = NAME.replace("_", "-")
VERSION = rf"""{NAME} {__version__}
Copyright (C) {datetime.now().year}
Written by Wu Zhenyu
"""
EPILOG = """
Report bugs to <wuzhenyu@ustc.edu>.
"""
SECTION = [
    ["BLACK", "YELLOW", r" \s \v"],
    ["WHITE", "BLACK", r"\S\? 󰀎 \u\?"],
    ["WHITE", "BLUE", r" \l"],
    ["BLACK", "WHITE", r" \w"],
]
SECTION_TEXT = "\n".join(
    " ".join(["--section"] + [repr(s) for s in section]) for section in SECTION
)


def get_parser() -> ArgumentParser:
    r"""Get a parser for unit test."""
    parser = ArgumentParser(
        description="""\
generate prompt by `translate_shell.utils.misc`'s `p10k_sections()`.
By default, it is for lftp. See section cmd:prompt of `man lftp`.
""",
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", version=VERSION, action="version")
    shtab.add_argument_to(parser)
    parser.add_argument(
        "--format",
        default="""# generated by `python -m translate_shell.tools.generate_prompt`
set prompt '{text}'
""",
        help="format the output. default: %(default)s",
    )
    parser.add_argument(
        "--prompt-string",
        default="\\n~> ",
        help="the suffix of prompt. default: %(default)s",
    )
    parser.add_argument(
        "--section",
        nargs="*",
        default=[],
        action="append",
        help=f"insert sections. default: {SECTION_TEXT}",
    )
    return parser


def main() -> None:
    r"""Parse arguments and provide shell completions."""
    parser = get_parser()
    args = parser.parse_args()

    import sys

    from ...utils.misc import p10k_sections

    if args.section == []:
        args.section = SECTION
    args.section = [
        section[0] if len(section) == 1 else section
        for section in args.section
    ]
    # sys.stdout.write will remove ANSI escape code when output is not a tty
    with sys.stdout as f:
        f.write(
            args.format.format(
                text=p10k_sections(args.section) + args.prompt_string  # type: ignore
            )
        )


if __name__ == "__main__":
    main()
