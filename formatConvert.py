"""
检测图片大小和格式
对提取到的图片进行格式转换，确保图片为可以被微信导入的gif格式
"""

import os
import imageio.v3 as iio

# 判断图片是否为gif格式
def is_gif_image(file_path):
    if file_path.lower().endswith('.gif'):
        return True
    return False

# 将图片转换为gif格式，输入路径由用户定义，默认输出到同一目录下的output文件夹中
def convert_image_to_gif(input_path, output_path):
    try:
        # 读取图片
        image = iio.imread(input_path)
        # 保存为 GIF 格式
        iio.imwrite(output_path, image, extension='.gif')
        print(f"转换成功: {input_path} -> {output_path}")
        return output_path
    except FileNotFoundError:
        print(f"错误: 输入文件未找到 - {input_path}")
    except Exception as e:
        print(f"转换失败: {input_path} -> {output_path}, 错误: {e}")

# 对图片进行压缩，如果图片大于500KB，则进行压缩处理
def compress_image(input_path, output_path, max_size_kb=500):
    try:
        # 读取图片
        image = iio.imread(input_path)
        # 检查图片大小
        size_kb = os.path.getsize(input_path) / 1024  # 转换为KB
        if size_kb > max_size_kb:
            # 使用较低的质量进行压缩
            iio.imwrite(output_path, image, palettesize=16, extension='.gif')
            size_kb = os.path.getsize(output_path) / 1024
            print(f"压缩成功: {input_path} -> {output_path}, 压缩后大小: {size_kb:.2f} KB")
            return output_path
        else:
            print(f"图片大小在限制内，无需压缩: {input_path}")
            return input_path
    except FileNotFoundError:
        print(f"错误: 输入文件未找到 - {input_path}")
    except Exception as e:
        print(f"压缩失败: {input_path} -> {output_path}, 错误: {e}")

if __name__ == "__main__":
    # 示例用法
    input_image_path = 'testcase/test_image.jpg'  # 输入图片路径
    output_image_path = 'testcase/test_image.gif'  # 输出图片路径

    convert_image_to_gif(input_image_path, output_image_path)
