import os
import sys
import binascii
from steam.core.manifest import DepotManifest

def decrypt_manifest_filenames(manifest_path, depot_key_hex):
    """
    解密Steam manifest文件中的文件名
    
    参数:
    manifest_path: manifest文件路径
    depot_key_hex: depot key (十六进制字符串)
    """
    # 检查文件是否存在
    if not os.path.exists(manifest_path):
        print(f"错误: 文件 '{manifest_path}' 不存在")
        return False
    
    try:
        # 将十六进制的depot key转换为bytes
        try:
            depot_key = binascii.unhexlify(depot_key_hex)
        except binascii.Error:
            print("错误: 无效的depot key格式，请提供有效的十六进制字符串")
            return False
        
        # 读取manifest文件
        print(f"读取manifest文件: {manifest_path}")
        with open(manifest_path, 'rb') as f:
            data = f.read()
        
        # 解析manifest
        print("解析manifest数据...")
        manifest = DepotManifest(data)
        
        # 检查文件名是否已加密
        if not manifest.filenames_encrypted:
            print("文件名未加密，无需解密")
            return True
        
        # 解密文件名
        print("开始解密文件名...")
        manifest.decrypt_filenames(depot_key)
        
        # 将修改后的manifest数据写回文件
        print("将解密后的manifest写回文件...")
        with open(manifest_path, 'wb') as f:
            f.write(manifest.serialize(compress=False))
        
        print("解密完成!")
        
        # 打印部分文件名作为验证
        file_count = len(manifest.payload.mappings)
        print(f"manifest包含 {file_count} 个文件")
        
        return True
    
    except Exception as e:
        print(f"错误: {str(e)}")
        return False

def main():
    # 检查命令行参数
    if len(sys.argv) != 3:
        print("用法: python raw_manifest_name_decrypt.py <manifest文件路径> <depot_key十六进制字符串>")
        manifest_path = input("请输入manifest文件路径: ")
        depot_key_hex = input("请输入depot key的十六进制字符串: ")
    else:
        manifest_path = sys.argv[1]
        depot_key_hex = sys.argv[2]
        
    decrypt_manifest_filenames(manifest_path, depot_key_hex)

if __name__ == "__main__":
    main()