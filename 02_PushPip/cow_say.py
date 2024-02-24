import argparse

import cowsay


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("message", type=str, nargs="*")

    parser.add_argument("-e", type=str, default=cowsay.Option.eyes)
    parser.add_argument("-f", type=str, default=None)

    parser.add_argument("-l", action="store_true")
    parser.add_argument("-n", action="store_true")

    parser.add_argument("-T", type=str, default=cowsay.Option.tongue)
    parser.add_argument("-W", type=str, default=40)

    parser.add_argument("-b", action="store_true")
    parser.add_argument("-d", action="store_true")
    parser.add_argument("-g", action="store_true")
    parser.add_argument("-p", action="store_true")
    parser.add_argument("-s", action="store_true")
    parser.add_argument("-t", action="store_true")
    parser.add_argument("-w", action="store_true")
    parser.add_argument("-y", action="store_true")

    args = parser.parse_args()

    if args.l:
        print(" ".join(cowsay.list_cows()))
    else:
        preset = "".join(
            [
                i
                for (i, flag) in zip(
                    "bdgpstwy",
                    [
                        args.b,
                        args.d,
                        args.g,
                        args.p,
                        args.s,
                        args.t,
                        args.w,
                        args.w,
                        args.y,
                    ],
                )
                if flag
            ]
        )

        if len(preset) == 0:
            preset = None
        else:
            preset = preset

        if len(args.message) == 0:
            raise RuntimeError("Empty message!")

        cow = "default"
        file = None
        if args.f is not None and "/" in args.f:
            file = args.f
        else:
            cow = args.f if args.f is not None else cow

        print(
            cowsay.cowsay(
                message=" ".join(args.message),
                cow=cow,
                preset=preset,
                eyes=args.e,
                tongue=args.T,
                width=args.W,
                wrap_text=args.n,
                cowfile=file,
            )
        )


if __name__ == "__main__":
    main()
