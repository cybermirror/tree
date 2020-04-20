import argparse
import os

# This Python script supports command line options using standard module argparse
# Type python tree.py -h to get the list of options.
# or python3 tree.py -h to get the list options.

# get_dirlist scans the current_dir using os.scandir() (available from Python 3.5) and
# construct the directory tree recursively using ├ , ─ , └ characters
#
# current_dir : the current directory to be scanned
# depth : number of sub-levels to be included in directory tree. When depth=1, will discontinue sub-directory scan
# indent : current level directory or file indent string and will be used to construct subdirectory indent,
#     next_indent. Initial indent should be "" to let the function to construct 1st indent with indent_space
# indent_space : the repetition before and after ├ (that is space and ─) for construction of next_indent. Minimum
#     is 1, default is 3. It is also equal to size of indent for each subdirectory
# folder_only : =True if only directory is shown in result
# silent_mode : default is False to print directory tree to screen. True to suppress print to screen
# prefix_dir_char : The prefix character add before the folder name. Default is the folder emoji
# prefix_file_char : The prefix character add before non-folder name. Default is memo emoji.
# prefix_symlink_char : The prefix character add before symlink file name. Default is link emoji.


def get_dirlist(current_dir,
                depth,
                indent="",
                indent_space=2,
                folder_only=False,
                include_period=False,
                silent_mode=False,
                prefix_dir_char="\N{OPEN FILE FOLDER}",
                prefix_file_char="\N{MEMO} ",
                prefix_symlink_char="\N{LINK SYMBOL}"):

    result_list = []

    if folder_only:
        if include_period:
            subitem_total = sum(1 for n in os.scandir(current_dir)
                                if n.is_dir())
        else:
            subitem_total = sum(1 for n in os.scandir(current_dir)
                                if n.is_dir() and (not n.name.startswith(".")))
    else:
        if include_period:
            subitem_total = sum(1 for n in os.scandir(current_dir))
        else:
            subitem_total = sum(1 for n in os.scandir(current_dir)
                                if (not n.name.startswith(".")))

    if indent_space < 1:
        indent_space = 1

    if indent == "":
        indent = " "*indent_space + "├" + "─"*indent_space

    subitem_count = 0
    with os.scandir(current_dir) as subdir:
        for subitem in subdir:
            if folder_only and (not subitem.is_dir()):
                continue
            if (not include_period) and subitem.name.startswith("."):
                continue
            subitem_count += 1
            # Construct the next level indent string, and if this directory is the end of parent folder
            # scan, change the tree character from ├" to "└"
            is1 = indent_space + 1
            if subitem_count == (subitem_total):    # last item in the subdir
                next_indent = indent[:-(is1)] + " "*(is1) + indent[-(is1):]
                indent = indent[:-(is1)] + "└" + "─"*(is1-1)
            else:    # not the last item in the subdir
                next_indent = indent[:-(is1)] + \
                    "│" + " "*indent_space + indent[-(is1):]
            if depth >= 1:  # not yet end of recursive sub-levels
                # determine leading character before directory / file name
                if subitem.is_file():
                    leading_char = prefix_file_char
                elif subitem.is_dir():
                    leading_char = prefix_dir_char
                elif subitem.is_symlink():
                    leading_char = prefix_symlink_char
                else:
                    leading_char = ""
                if not silent_mode:
                    print(f"{indent}{leading_char}{subitem.name}")
                result_list.append(f"{indent}{leading_char}{subitem.name}\n")

                # Recursively scan sub-directory
                if subitem.is_dir():
                    result_list.extend(get_dirlist(subitem,
                                                   depth-1,
                                                   next_indent,
                                                   indent_space,
                                                   folder_only,
                                                   include_period,
                                                   silent_mode,
                                                   prefix_dir_char,
                                                   prefix_file_char,
                                                   prefix_symlink_char))
    return result_list


my_parser = argparse.ArgumentParser(
    prog="python tree.py",
    # usage="%(prog)s [options] path",
    description="List folder content recursively in tree structure",
    # epilog="For any question, pls email to me",
    allow_abbrev=False)

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
my_parser.add_argument("-w", "--writetofile",
                       action="store_true",
                       required=False,
                       help="Write the tree to file")
my_parser.add_argument("-o", "--outputfile", metavar="FILENAME",
                       action="store",
                       type=str,
                       default="FOLDER_LIST.txt",
                       required=False,
                       help="Specify output file name if \
                       other than FOLDER_LIST.txt")
my_parser.add_argument("-e", "--emoji",
                       action="store_true",
                       required=False,
                       help="Add emoji as prefix to folder/file names")
my_parser.add_argument("-v", "--version",
                       action="version",
                       version="0.1.0")

args = my_parser.parse_args()

if args.emoji:
    folder_char = "\N{OPEN FILE FOLDER}"
    file_char = "\N{MEMO}"
    symlink_char = "\N{LINK SYMBOL}"
else:
    folder_char = ""
    file_char = ""
    symlink_char = ""

if not os.path.exists(args.path):
    print(f"{args.path} does not exists.")
elif not os.path.isdir(args.path):
    print(f"{args.path} is not directory")
else:
    output_file = args.outputfile
    if output_file.lower().endswith(".txt"):
        original_file = output_file[:-4]
    else:
        original_file = output_file
        output_file = original_file + ".txt"

    n = 0
    while os.path.exists(output_file):
        output_file = f"{original_file}_{n:03}.txt"
        n += 1

    if not args.silent:
        print(f"\n{os.path.abspath(args.path)}")

    if args.writetofile:
        with open(output_file, mode="w", encoding="utf-8-sig") as f:
            f.write(
                f"Directory list of {args.path} upto {args.depth} sub-level(s)\n")
            f.write(f"List folder only : {args.folderonly}\n\n")
            f.write(f"{os.path.abspath(args.path)}\n")
            f.writelines(get_dirlist(args.path, args.depth, indent="",
                                     indent_space=args.indent,
                                     folder_only=args.folderonly,
                                     include_period=args.period,
                                     silent_mode=args.silent,
                                     prefix_dir_char=folder_char,
                                     prefix_file_char=file_char,
                                     prefix_symlink_char=symlink_char))
        print(
            f"\nDirectory list is written to text file: {os.path.abspath(output_file)}\n")
    else:
        get_dirlist(args.path, args.depth, indent="",
                    indent_space=args.indent,
                    folder_only=args.folderonly,
                    include_period=args.period,
                    silent_mode=args.silent,
                    prefix_dir_char=folder_char,
                    prefix_file_char=file_char,
                    prefix_symlink_char=symlink_char)
