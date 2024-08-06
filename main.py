from datetime import datetime, timedelta
import os
import exiftool
import sys
import re
from shutil import copyfile
from PIL import Image
from pillow_heif import register_heif_opener
import time
import dateparser


def converth2j(heicf, jpgf):
    try:
        register_heif_opener()
        im = Image.open(heicf)
        # Save the image as JPG
        with open(jpgf, "wb") as jpg_file:
            im.save(jpg_file, "JPEG", quality=100)
    except Exception as e:
        print(f"Error converting {heicf}: {str(e)}")


def renameMMExportFile(file):
    newfl = file.split("mmexport")
    newf = newfl[1]
    # convert milsecond timestamp to datetime str
    try:
        newf = datetime.fromtimestamp(
            int(newf.split(".")[0])/1000).strftime("%Y%m%d_%H%M%S") + os.path.splitext(newf)[1]
        os.replace(file, newfl[0]+newf)
        return newf
    except Exception as e:
        print(f"Error renaming {file}: {str(e)}")
        return file


def rename8_6(file):
    basename = os.path.basename(file)
    match = re.search(r'\d{8}_\d{6}', basename)
    bvalidname = False
    if match:
        basename = os.path.basename(file)
        dirname = os.path.dirname(file)
        newfile = os.path.join(
            dirname, match.group(0)+os.path.splitext(basename)[1])
        if newfile == file:
            return file, True
        os.replace(file, newfile)
        bvalidname = True
        file = newfile
    return file, bvalidname


def rename14(file):
    basename = os.path.basename(file)
    match = re.search(r'\d{14}', basename)
    if match:
        basename = os.path.basename(file)
        dirname = os.path.dirname(file)
        newfile = os.path.join(
            dirname,  match.group(0)[:8] + "_" + match.group(0)[8:]+os.path.splitext(basename)[1])

        while True:
            if (not os.path.exists(newfile)):
                os.replace(file, newfile)
                break
            else:
                basename = os.path.splitext(os.path.basename(newfile))[0]
                dt = datetime.strptime(match.group(0), "%Y%m%d%H%M%S")
                dt += timedelta(seconds=1)
                dt_str = dt.strftime("%Y%m%d_%H%M%S")
                newfile = os.path.join(
                    dir_name, dt_str+os.path.splitext(newfile)[1])
        file = newfile
    return file


def renameYdahMdashDdashhdashmdashs(file):
    basename = os.path.basename(file)
    match = re.search(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}', basename)
    if match:
        ext = os.path.splitext(file)[1]
        basename_noext = match.group(0).replace("-", "")
        dirname = os.path.dirname(file)
        basename_noext = basename_noext[:8] + "_" + basename_noext[8:]

        newfile = os.path.join(dirname, basename_noext + ext)

        while True:
            if (not os.path.exists(newfile)):
                os.replace(file, newfile)
                break
            else:
                basename = os.path.splitext(os.path.basename(newfile))[0]
                dt = datetime.strptime(match.group(0), "%Y%m%d%H%M%S")
                dt += timedelta(seconds=1)
                dt_str = dt.strftime("%Y%m%d_%H%M%S")
                newfile = os.path.join(
                    dir_name, dt_str+os.path.splitext(newfile)[1])
        file = newfile
    return file


def rename2YdashMdashDblankhdashmdashs(file):
    basename = os.path.basename(file)
    match = re.search(r'\d{2}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}', basename)
    if match:
        newbasename_noext = "20" + \
            match.group(0).replace("-", "").replace(" ", "_")
        ext = os.path.splitext(basename)[1]
        dirname = os.path.dirname(file)
        newfile = os.path.join(dirname, newbasename_noext + ext)

        while True:
            if (not os.path.exists(newfile)):
                os.replace(file, newfile)
                break
            else:
                basename = os.path.splitext(os.path.basename(newfile))[0]
                dt = datetime.strptime(match.group(0), "%Y%m%d%H%M%S")
                dt += timedelta(seconds=1)
                dt_str = dt.strftime("%Y%m%d_%H%M%S")
                newfile = os.path.join(
                    dir_name, dt_str+os.path.splitext(newfile)[1])
        file = newfile
    return file


def renameYdashMdashDhms(file):
    basename = os.path.basename(file)
    match = re.search(r'\d{4}-\d{2}-\d{2} \d{6}', basename)
    if match:
        basename_noext = match.group(0).replace("-", "").replace(" ", "_")
        ext = os.path.splitext(basename)[1]
        dirname = os.path.dirname(file)

        newfile = os.path.join(dirname, basename_noext + ext)

        while True:
            if (not os.path.exists(newfile)):
                os.replace(file, newfile)
                break
            else:
                basename = os.path.splitext(os.path.basename(newfile))[0]
                dt = datetime.strptime(match.group(0), "%Y-%m-%d %H%M%S")
                dt += timedelta(seconds=1)
                dt_str = dt.strftime("%Y%m%d_%H%M%S")
                newfile = os.path.join(
                    dir_name, dt_str+os.path.splitext(newfile)[1])
        file = newfile
    return file


def rename8(file):
    try:
        basename = os.path.basename(file)
        match = re.search(r'\d{8}', basename)
        if match:
            basename_noext = match.group(0)+"_"+"235959"
            ext = os.path.splitext(basename)[1]
            dirname = os.path.dirname(file)

            newfile = os.path.join(dirname, basename_noext + ext)

            while True:
                if (not os.path.exists(newfile)):
                    os.replace(file, newfile)
                    break
                else:
                    basename = os.path.splitext(os.path.basename(newfile))[0]
                    dt = datetime.strptime(basename, "%Y%m%d_%H%M%S")
                    dt += timedelta(seconds=1)
                    dt_str = dt.strftime("%Y%m%d_%H%M%S")
                    newfile = os.path.join(
                        dir_name, dt_str+os.path.splitext(newfile)[1])
            file = newfile
    except Exception as e:
        print(f"Error renaming(rename8) {file}: {str(e)}")

    return file


def moveInCalDir(abp_file, todir):
    f = abp_file
    filename = f.split(os.sep)[-1].split("___")[-1].lower()
    # filename = filename_bk.lower()
    filename_l = list(os.path.splitext(filename))

    # if filename_l[-1] in (".jpg", ".jpeg", ".png"):
    #     filename_l[-1] = '.jpg'

    # if filename_l[-1] != ".jpg":
    #     raise Exception("Not a target-type photo")

    dt = datetime.strptime(filename_l[0], "%Y%m%d_%H%M%S")
    newdir = os.path.join(todir, "{:04}".format(
        str(dt.year)), "{:02}".format(dt.month))

    # recursively create dir if newdir doesnt exist
    if not os.path.exists(newdir):
        os.makedirs(newdir)

    newfile = os.path.join(newdir, "".join(filename_l))
    os.replace(f, newfile)
    # os.replace(f, newfile)
    # while True:
    #     if (not os.path.exists(newfile)):
    #         os.replace(f, newfile)
    #         break
    #     else:
    #         basename_noext, ext = os.path.splitext(os.path.basename(newfile))
    #         dt = datetime.strptime(basename_noext, "%Y%m%d_%H%M%S")
    #         dt += timedelta(seconds=1)
    #         dt_str = dt.strftime("%Y%m%d_%H%M%S")
    #         newfile = os.path.join(
    #             os.path.dirname(newfile), dt_str+ext)
    #     file = newfile


def absoluteFilePaths(directory):
    a = os.walk(directory)
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def updateDatetimeOri(dt, file):
    with exiftool.ExifToolHelper(executable=abp_exiftool) as tool:
        datetimeori_readable = dt.strftime("%Y:%m:%d %H:%M:%S")
        datetimeori_bytes = (
            "-DateTimeOriginal=" + datetimeori_readable).encode('utf-8')
        software_bytes = ("-Software=tomtstool").encode('utf-8')
        tool.execute(datetimeori_bytes, software_bytes,
                     file, "-overwrite_original")


# def updateTrackCreateOri(dt, file):
#     with exiftool.ExifToolHelper(executable=abp_exiftool) as tool:
#         datetimeori_readable = dt.strftime("%Y:%m:%d %H:%M:%S")
#         datetimeori_bytes = (
#             "-TrackCreateDate=" + datetimeori_readable).encode('utf-8')
#         software_bytes = ("-Software=tomtstool").encode('utf-8')
#         tool.execute(datetimeori_bytes, software_bytes,
#                      file, "-overwrite_original")


# def addDatetimeOri(file):
#     with exiftool.ExifToolHelper(executable=abp_exiftool) as tool:
#         key_datetimeori, key_software = (
#             "EXIF:DateTimeOriginal", "EXIF:Software")
#         metadata = tool.get_metadata(file)
#         d = metadata[0]
#         if key_datetimeori not in d:
#             # time.sleep(1)
#             datetimeori_readable = datetime.now().strftime(
#                 "%Y:%m:%d %H:%M:%S")
#             datetimeori_bytes = (
#                 "-DateTimeOriginal=" + datetimeori_readable).encode('utf-8')
#             software_bytes = ("-Software=tomtstool").encode('utf-8')
#             tool.execute(datetimeori_bytes, software_bytes,
#                          abp_file, "-overwrite_original")


currentdir = os.path.dirname(os.path.abspath(__file__))
dir_name = "photodir"
donept_dir_name = "donephotos"
all_files = absoluteFilePaths(dir_name)
abp_exiftool = r'F:\photo_script\exiftool\exiftool(-k).exe'
currenttime = datetime.now()
currenttime = currenttime.strftime(
    "%Y%m%d_%H%M%S_") + str(currenttime.microsecond)


all_files = list(all_files)
count = 0
startdt = datetime.now()
for abp_file in all_files:

    nowdt = datetime.now()
    count += 1
    # seconds after startdt
    laps = (nowdt - startdt).total_seconds()
    percent = count/len(all_files)

    print("No.{} file {:0.2f}% {:0.1f}sec remain".format(
        count, percent*100, laps/percent - laps).center(80, '-'))
    print("{:15.15}{}".format("abp_file:", abp_file))
    # get file name from absolute path
    print("{:15.15}{}".format(
        "file:", os.path.basename(abp_file)))
    if abp_file.find("mmexport") != -1:
        abp_file = renameMMExportFile(abp_file)

    abp_file_bk = abp_file
    abp_file, bvalidname = rename8_6(abp_file)
    if (abp_file == abp_file_bk and not bvalidname):
        abp_file = rename14(abp_file)
    if (abp_file == abp_file_bk and not bvalidname):
        abp_file = renameYdashMdashDhms(abp_file)
    if (abp_file == abp_file_bk and not bvalidname):
        abp_file = rename2YdashMdashDblankhdashmdashs(abp_file)
    if (abp_file == abp_file_bk and not bvalidname):
        abp_file = rename8(abp_file)
    if (abp_file == abp_file_bk and not bvalidname):
        dirname = os.path.dirname(abp_file)
        abpname_noex, ext = os.path.splitext(os.path.basename(abp_file))
        abpname_noex = abpname_noex.replace(
            "_", "").replace("-", "").replace(" ", "")
        abp_file = os.path.join(dirname, abpname_noex+ext)
        os.replace(abp_file_bk, abp_file)
        abp_file = rename14(abp_file)

    if abp_file_bk != abp_file:
        try:
            abp_file_noext = os.path.splitext(os.path.basename(abp_file))[0]
            datetime.strptime(abp_file_noext, "%Y%m%d_%H%M%S")
        except Exception as e:
            os.replace(abp_file, abp_file_bk)
            abp_file = abp_file_bk

    print("{:15.15}{} {}".format(
        "Info:", "file name after rename is", os.path.basename(abp_file)))
    if abp_file != abp_file_bk:
        print("{:15.15}from:{} to:{}".format("renamed_file:",
              os.path.basename(abp_file_bk), os.path.basename(abp_file)))

    try:
        with exiftool.ExifToolHelper(executable=abp_exiftool) as tool:
            metadata = tool.get_metadata(abp_file,)
            for d in metadata:
                # identify it's a photo first
                key_filetype, key_filetypeext, key_mimetype, key_datetimeori, key_software, key_trackcreate = (
                    "File:FileType", "File:FileTypeExtension", "File:MIMEType", "EXIF:DateTimeOriginal", "EXIF:Software", "QuickTime:CreateDate")

                if key_filetype in d:
                    bimage = False
                    bvideo = False
                    if d[key_filetype] == "HEIC":
                        abp_file_jpg = os.path.splitext(abp_file)[0] + ".jpg"
                        # convert abp_file to jpg
                        converth2j(heicf=abp_file, jpgf=abp_file_jpg)
                        tool.execute(
                            *["-tagsfromfile", abp_file, "--exif:Orientation", abp_file_jpg, "-overwrite_original"])

                        os.remove(abp_file)
                        abp_file = abp_file_jpg
                        d = tool.get_metadata(abp_file)[0]

                    if d[key_filetype] in ("JPEG", "PNG", "GIF"):
                        bimage = True
                    if d[key_filetype] in ("MP4", "MOV", "MPEG"):
                        bvideo = True

                    if not bimage and not bvideo:
                        print("{:15.15}{}".format(
                            "ERROR:", "Not a target-type"))
                        abp_newfilename = os.sep.join([os.path.dirname(os.path.abspath(
                            __file__)), "brokenphotodir", "other_filetype", "___".join(abp_file.split(os.sep)[3:])])
                        os.replace(abp_file, abp_newfilename)
                        continue

                    extmap = {"JPEG": ".jpg", "PNG": ".png",
                              "MP4": ".mp4", "MOV": ".mov", "MPEG": ".mpg", "GIF": ".gif"}
                    for k, v in extmap.items():
                        if d[key_filetype] == k and os.path.splitext(abp_file)[1] != v:
                            abp_newfilename = os.path.splitext(abp_file)[0] + v
                            os.replace(abp_file, abp_newfilename)
                            abp_file = abp_newfilename
                            print("{:15.15}{}".format(
                                "updated_file_ext:", os.path.basename(abp_file)))
                            break

                    key_exifcreate = "QuickTime:CreateDate" if bvideo else "EXIF:DateTimeOriginal"
                    if key_exifcreate not in d or "0000" in d[key_exifcreate]:
                        exifcreate_readable = datetime.now().strftime(
                            "%Y:%m:%d %H:%M:%S")
                        exifkey_tocall = "-DateTimeOriginal" if bimage else "-CreateDate"
                        exifcreate_bytes = (
                            exifkey_tocall + "=" + exifcreate_readable).encode('utf-8')
                        tool.execute(exifcreate_bytes, abp_file,
                                     "-overwrite_original")
                        d = tool.get_metadata(abp_file)[0]

                    # get modified time
                    mtime = os.path.getmtime(abp_file)
                    mtime_readable = datetime.fromtimestamp(mtime)
                    print("{:15.15}{}".format(
                        "mtime:", mtime_readable))

                    # get create time
                    ctime = os.path.getctime(abp_file)
                    ctime_readable = datetime.fromtimestamp(ctime)
                    print("{:15.15}{}".format(
                        "ctime:", ctime_readable))

                    # get exif datetime original
                    exifkey = key_datetimeori if bimage else key_trackcreate
                    exifcreate_readable = d[exifkey]
                    exifcreate = datetime.strptime(
                        exifcreate_readable, "%Y:%m:%d %H:%M:%S")
                    print("{:15.15}{}".format(
                        exifkey+":", exifcreate_readable))

                    filen_dt_readable = ""
                    filen_dt = datetime.max
                    # if key_software in d and d[key_software] == "Picasa":
                    suspicious_filename_datetime = os.path.splitext(
                        os.path.basename(abp_file))[0]
                    if re.match(r'^\d{8}_\d{6}$', suspicious_filename_datetime):
                        filen_dt_readable = suspicious_filename_datetime
                        print("{:15.15}{}".format(
                            "fname_dtime:", filen_dt_readable))
                        filen_dt = datetime.strptime(
                            filen_dt_readable, '%Y%m%d_%H%M%S')
                    else:
                        print(suspicious_filename_datetime)

                    if bvideo:
                        # exifcreate add 8 hours  Hack for timezone
                        exifcreate += timedelta(hours=8)
                    mindatetime = min(
                        exifcreate, ctime_readable, mtime_readable, filen_dt)
                    if mindatetime != exifcreate:
                        # hack for live photo
                        # if exifcreate is no late than mindatetime for 600 secs
                        if bvideo and (exifcreate - mindatetime).total_seconds() < 600:
                            print("{:15.15}{}".format(
                                "INFO:", "exifcreate is no late than mindatetime for 600 secs"))
                            mindatetime = exifcreate
                        else:
                            laps = (exifcreate - mindatetime).total_seconds()
                            print("{:15.15}{}".format(
                                "INFO:", "exifcreate is late than mindatetime for {} secs".format(laps)))
                            exifcreate_readable = mindatetime.strftime(
                                "%Y:%m:%d %H:%M:%S")
                            exifkey_tocall = "-DateTimeOriginal" if bimage else "-CreateDate"
                            exifcreate_bytes = (
                                exifkey_tocall + exifcreate_readable).encode('utf-8')
                            tool.execute(exifcreate_bytes, abp_file,
                                         "-overwrite_original")
                            # done
                            print("{:15.15}{}".format(
                                "DONE:", "datetime original updated"))

                    abpname_noex, extension = os.path.splitext(abp_file)
                    spl = abpname_noex.split(os.sep)
                    spl[-1] = mindatetime.strftime("%Y%m%d_%H%M%S")
                    temp_abp_filename = os.sep.join(spl) + extension
                    if abp_file != temp_abp_filename:
                        os.replace(abp_file, temp_abp_filename)
                        abp_file = temp_abp_filename
                    print("{:15.15}{}".format(
                        "FINAL NAME:", os.path.basename(abp_file)))
                    moveInCalDir(abp_file, os.path.join(
                        currentdir, donept_dir_name))

    except Exception as e:
        print("{:15.15}{}".format(
            "Exception Name:", e))
        print("{:15.15}{}".format(
            "Exception:", "error with file {}".format(abp_file)))

        if isinstance(e, UnicodeDecodeError) and e.reason == "illegal multibyte sequence" and e.encoding == "gbk":
            abp_newfilename = os.sep.join([os.path.dirname(os.path.abspath(
                __file__)), "brokenphotodir", "gbk_encoding", "___".join(abp_file.split(os.sep)[3:])])
            # os.replace(abp_file, abp_newfilename)

            brokenfilelog = "logs/brokenfile_illegal_mul_seq_" + currenttime + ".log"
            with open(brokenfilelog, "a") as f:
                f.write(abp_newfilename + "\n")
        else:
            print("Some else error!!!")
