import argparse
from os.path import isdir
from cobra_ssg import cobra_render

def main():
    parser = argparse.ArgumentParser(description="Cobra Static Site Generator")
    parser.add_argument("-s", "--source", type=str, default="content", help="Path of the content folder (default: content)")
    parser.add_argument("-b", "--build", type=str, default="build", help="Path of the build folder (default: build)")
    args = parser.parse_args()

    if not isdir(args.source):
        print(f"There is no source folder {args.source}")
        exit()

    try:
        cobra_render(source_folder=args.source, build_folder=args.build)
        print(f"Site successfully built in '{args.build}' folder.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
