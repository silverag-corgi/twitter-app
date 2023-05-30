import argparse
import os
import sys
from typing import Optional

import decli
import python_lib_for_me as pyl

from twitter_app.main import argument_parser_info


def main() -> int:
    clg: Optional[pyl.CustomLogger] = None

    try:
        # ロガーの取得
        clg = pyl.CustomLogger(__name__)

        # コマンドの表示
        sys.argv[0] = os.path.basename(sys.argv[0])
        clg.log_inf(f"コマンド：{sys.argv}")

        # 引数の解析
        parser: pyl.CustomArgumentParser = decli.cli(
            argument_parser_info.ARGUMENT_PARSER_INFO_DICT,
            pyl.CustomArgumentParser,
        )
        if len(sys.argv) == 1:  # サブコマンドが指定されていない場合
            parser.print_help()
            return 0
        arg_namespace: argparse.Namespace = parser.parse_args()

        # サブコマンドの実行
        arg_namespace.func(arg_namespace)
    except KeyboardInterrupt as e:
        if clg is not None:
            clg.log_inf(f"処理を中断しました。")
        return 1
    except pyl.ArgumentValidationError as e:
        if clg is not None:
            clg.log_err(f"{e}")
        return 1
    except Exception as e:
        if clg is not None:
            clg.log_exc("")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
