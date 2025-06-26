from getQQEmo import *
from formatConvert import convert_image_to_gif as cg
from formatConvert import compress_image as cm
from formatConvert import is_gif_image
from autAdding import auto_add
import os

def main():
    # 获取用户QQ指定账号的数据目录
    qq_userdata_dir = get_userdata_save_path()
    if not qq_userdata_dir:
        print("无法获取QQ用户数据目录")
        sys.exit(1)

    selected_dir = select_userdata_dir_main(qq_userdata_dir)
    if not selected_dir:
        print("未选择任何QQ账号数据目录")
        sys.exit(1)

    file_path = Path(selected_dir)
    # 拼接表情的绝对路径
    emoji_path = file_path / "nt_qq" / "nt_data" / "Emoji" / "personal_emoji" / "Ori"
    print(f"该账号的表情目录绝对路径为：{emoji_path}")
    # 设置并指定保存的目录
    save_path = "emo"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    sleep(0.5)
    print("开始复制文件……")
    copy_directory_with_progress(emoji_path, save_path)
    print("复制完成！开始重命名文件……")
    sleep(0.5)
    batch_correct_extensions(save_path)
    print("复制文件完成！正在打开输出文件夹……")
    try:
        subprocess.Popen(['explorer', os.path.abspath(save_path)])
    except Exception as e:
        print(f"无法打开资源管理器: {e}")

    path_afterprocess = "emo_afterprocess"
    if not os.path.exists(path_afterprocess):
        os.makedirs(path_afterprocess)

    # 检查所有表情包大小和格式，并进行格式转换
    # # 创建一个gif的子文件夹作为输出路径，将所有转换后的gif文件存放在这里
    # output_path = os.path.join('converted_gif')
    # if not os.path.exists(output_path):
    #     os.makedirs(output_path)
    for root, dirs, files in os.walk(save_path):
        
        for file in files:
            file_path = os.path.join(root, file)
            # 检查文件格式并转换为gif
            if not is_gif_image(file_path):
                print(f"正在转换文件: {file_path}")
                # 将转换后的文件存放在指定的输出路径
                output_file = os.path.join(path_afterprocess, f"{os.path.splitext(file)[0]}.gif")
                cg(file_path, output_file)
                # 压缩图片
                cm(output_file, output_file)
            else:
                output_file = os.path.join(path_afterprocess, file)
                # 压缩图片
                cm(file_path, output_file)

    # 暂停程序，等待用户完成操作
    input("所有表情包已处理完成，请将所有gif文件导入微信中。等待用户完成操作...")

    # 启动脚本，开始自动化导入表情包
    file_count = 0
    for root, dirs, files in os.walk('emo_afterprocess'):
        file_count += len(files)
    auto_add(file_count)

if __name__ == "__main__":
    main()
    