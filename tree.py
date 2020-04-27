from datetime import datetime
from pathlib import Path
import argparse


# This Python script supports command line options using standard module argparse
# Type python tree.py -h to get the list of options.
# or python3 tree.py -h to get the list options.

# get_dirlist scans the current_dir using path_obj.iterdir() (available from pathlib) and
# construct the directory tree recursively using ├ , ─ , └ characters
# get_dirlist is iterable constructor
#
# current_dir : the current directory to be scanned
# depth : number of sub-levels to be included in directory tree. When depth=1, will discontinue sub-directory scan
# indent : current level directory or file indent string and will be used to construct subdirectory indent,
#     next_indent. Initial indent should be "" to let the function to construct 1st indent with indent_space
# indent_space : the repetition before and after ├ (that is space and ─) for construction of next_indent. Minimum
#     is 1, default is 3. It is also equal to size of indent for each subdirectory
# folder_only : =True if only directory is shown in result
# exclude_file_prefix : excldue files with prefix found in exclude_file_prefix. Default is ".@"
# prefix_dir_char : The prefix character add before the folder name. Default is the folder emoji
# prefix_file_char : The prefix character add before non-folder name. Default is memo emoji.


def get_dirlist(current_dir,
                depth,
                indent="",
                indent_space=2,
                indent_prefix="",
                folder_only=False,
                exclude_file_prefix=".@",
                prefix_dir_char="\N{OPEN FILE FOLDER}",
                prefix_file_char="\N{MEMO} "):

    if folder_only:
        if exclude_file_prefix == "":
            subitem_total = sum(1 for n in current_dir.iterdir() if n.is_dir())
        else:
            subitem_total = sum(1 for n in current_dir.iterdir()
                                if n.is_dir() and (n.name[0] not in exclude_file_prefix))
    else:
        if exclude_file_prefix == "":
            subitem_total = sum(1 for n in current_dir.iterdir())
        else:
            subitem_total = sum(1 for n in current_dir.iterdir()
                                if (n.name[0] not in exclude_file_prefix))

    if indent_space < 1:
        indent_space = 1

    if indent == "":
        indent = indent_prefix + " "*indent_space + "├" + "─"*indent_space

    subitem_count = 0
    for subitem in current_dir.iterdir():
        if folder_only and (not subitem.is_dir()):
            continue
        if (exclude_file_prefix != ""):
            if subitem.name[0] in exclude_file_prefix:
                continue
        subitem_count += 1
        # Construct the next level indent string,
        # and if this directory is the end of folder
        # scan, change the tree character from ├" to "└"
        is1 = indent_space + 1
        if subitem_count == (subitem_total):    # last item in the subdir
            next_indent = indent[:-(is1)] + indent_prefix + \
                " "*(is1) + indent[-(is1):]
            indent = indent[:-(is1)] + "└" + "─"*(is1-1)
        else:    # not the last item in the subdir
            next_indent = indent[:-(is1)] + \
                "│" + indent_prefix + " "*indent_space + indent[-(is1):]
        if depth >= 1:  # not yet end of recursive sub-levels
            # determine leading character before directory / file name
            if subitem.is_file():
                leading_char = prefix_file_char
            elif subitem.is_dir():
                leading_char = prefix_dir_char
            else:
                leading_char = ""
            # print(f"{indent}{leading_char}{subitem.name}")
            # result_list.append(f"{indent}{leading_char}{subitem.name}\n")
            yield f"{indent}{leading_char}{subitem.name}\n"
            # Recursively scan sub-directory
            if subitem.is_dir():
                yield from get_dirlist(subitem,
                                       depth-1,
                                       next_indent,
                                       indent_space,
                                       indent_prefix,
                                       folder_only,
                                       exclude_file_prefix,
                                       prefix_dir_char,
                                       prefix_file_char)


my_parser = argparse.ArgumentParser(
    prog="python tree.py",
    # usage="%(prog)s [options] path",
    description="List folder content recursively in tree structure",
    # epilog="For any question, pls email to me",
    allow_abbrev=False)
my_group = my_parser.add_mutually_exclusive_group(required=False)

my_parser.add_argument("path", nargs='?', metavar="PATH",
                       action="store",
                       type=str,
                       default=".",
                       help='Folder path. Default is current path')
my_parser.add_argument("-d", "--depth", metavar="INT",
                       action="store",
                       type=int,
                       default=1,
                       required=False,
                       help="Level(s) of sub-folders to be listed")
my_parser.add_argument("-i", "--indent", metavar="INT",
                       action="store",
                       type=int,
                       default=2,
                       required=False,
                       help="Indent character width of each sub-level")
my_parser.add_argument("-f", "--folderonly",
                       action="store_true",
                       required=False,
                       help="List folders only")
my_parser.add_argument("-p", "--period",
                       action="store_true",
                       required=False,
                       help="Include folder/file names started with '.'")
my_parser.add_argument("-s", "--silent",
                       action="store_true",
                       required=False,
                       help="Don't show result on screen")
my_parser.add_argument("-o", "--outputfile", metavar="FILENAME",
                       action="store",
                       type=str,
                       default="FOLDER_LIST",
                       required=False,
                       help="Specify output file name if \
                       other than 'FOLDER_LIST'")
my_parser.add_argument("-e", "--emoji",
                       action="store_true",
                       required=False,
                       help="Add emoji as prefix to folder/file names")
my_parser.add_argument("-v", "--version",
                       action="version",
                       version="0.1.0")

my_group.add_argument("-t", "--textfile",
                      action="store_true",
                      help="Write to text file")
my_group.add_argument("-c", "--csv",
                      action="store_true",
                      help="Write to csv file")
my_group.add_argument("-b", "--tab",
                      action="store_true",
                      help="Write to tsv file")


args = my_parser.parse_args()

input_path = Path(args.path)
full_path = input_path.resolve(strict=False)

if args.period:
    exclude_fp = ""
else:
    exclude_fp = ".@"


if args.emoji:
    folder_char = "\N{OPEN FILE FOLDER}"
    file_char = "\N{MEMO}"
else:
    folder_char = ""
    file_char = ""

if not input_path.exists():
    print(f"{str(input_path)} does not exists.")
elif not input_path.is_dir():
    print(f"{args.path} is not directory")
else:
    writetofile = True
    delimiter = ""
    if args.textfile:
        ext = ".txt"
    elif args.csv:
        ext = ".csv"
        delimiter = ","
    elif args.tab:
        ext = ".tsv"
        delimiter = "\t"
    else:
        writetofile = False

    if not args.silent:
        print(f"\n{str(full_path)}")
        for line in get_dirlist(input_path, args.depth, indent="",
                                indent_space=args.indent,
                                indent_prefix="",
                                folder_only=args.folderonly,
                                exclude_file_prefix=exclude_fp,
                                prefix_dir_char=folder_char,
                                prefix_file_char=file_char):
            print(line, end="")

    if writetofile:
        output_file = args.outputfile
        if output_file.lower().endswith(ext):
            original_file = output_file[:-4]
        else:
            original_file = output_file
            output_file = original_file + ext

        n = 0
        while Path(output_file).exists():
            output_file = f"{original_file}_{n:03}{ext}"
            n += 1

        now = datetime.now()
        print(f"\nWriting folder tree to file {str(output_file)}")

        with open(output_file, mode="w", encoding="utf-8-sig") as f:
            f.write(
                f"Directory list of {args.path} upto {args.depth} sub-level(s)\n")
            f.write(f"List folder only : {args.folderonly}\n")
            f.write(f"Date of listing: {now.strftime('%Y-%m-%d %I:%M %p')}\n")
            f.write(f"{str(full_path)}\n")
            f.writelines(get_dirlist(input_path, args.depth, indent="",
                                     indent_space=args.indent,
                                     indent_prefix=delimiter,
                                     folder_only=args.folderonly,
                                     exclude_file_prefix=exclude_fp,
                                     prefix_dir_char=folder_char,
                                     prefix_file_char=file_char))
        print(
            f"\nFolder tree has been written to file: {output_file}\n")
