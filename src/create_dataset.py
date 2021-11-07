from utils.python import bbox_tool, convert, structure_dataset,  process

_TRAIN_SIZE = 10


def main():
    bbox_tool.main()
    convert.main()
    structure_dataset.main()
    process.main(_TRAIN_SIZE)


if __name__ == '__main__':
    main()