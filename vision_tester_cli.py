from argparse import ArgumentParser


def get_parser():
    parser = ArgumentParser(description='vision tester cli')
    parser.add_argument('command', type=str, help='')
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    print(args.command)
