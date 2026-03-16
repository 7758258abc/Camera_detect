import cv2
import sys

def list_cameras():
    """检测可用的摄像头"""
    available_cameras = []
    for i in range(10):  # 检测0-9号摄像头
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                available_cameras.append(i)
                print(f"✓ 发现摄像头 {i}: 分辨率 {frame.shape[1]}x{frame.shape[0]}")
            cap.release()
    return available_cameras

def open_camera(camera_id=0):
    """打开指定摄像头"""
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"错误：无法打开摄像头 {camera_id}")
        return None
    
    # 设置分辨率（可选）
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    return cap

def main():
    print("=" * 50)
    print("USB 摄像头测试程序")
    print("=" * 50)
    
    # 1. 列出可用摄像头
    print("\n正在检测摄像头...")
    cameras = list_cameras()
    
    if not cameras:
        print("未检测到任何摄像头！")
        print("请检查：")
        print("  - USB摄像头是否正确连接")
        print("  - 摄像头是否被其他程序占用")
        sys.exit(1)
    
    # 2. 选择摄像头
    camera_id = cameras[0]  # 默认使用第一个
    if len(cameras) > 1:
        print(f"\n找到 {len(cameras)} 个摄像头")
        try:
            choice = int(input(f"请选择要使用的摄像头编号 {cameras}: "))
            if choice in cameras:
                camera_id = choice
        except ValueError:
            pass
    
    # 3. 打开摄像头
    print(f"\n正在打开摄像头 {camera_id}...")
    cap = open_camera(camera_id)
    if cap is None:
        sys.exit(1)
    
    # 获取实际分辨率
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"摄像头已启动: {width}x{height} @ {fps}fps")
    print("\n操作说明：")
    print("  [空格键] 拍照保存")
    print("  [Q/ESC]  退出程序")
    print("-" * 50)
    
    # 4. 主循环
    photo_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("错误：无法读取画面")
            break
        
        # 在画面上显示信息
        display_frame = frame.copy()
        cv2.putText(display_frame, f"Camera {camera_id} | {width}x{height}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, "SPACE:Photo | Q:Quit", 
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # 显示画面
        cv2.imshow('USB Camera', display_frame)
        
        # 按键处理
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' ') or key == ord('p'):  # 空格或P键拍照
            photo_count += 1
            filename = f"photo_{photo_count:03d}.jpg"
            cv2.imwrite(filename, frame)
            print(f"📷 已保存: {filename}")
            
        elif key == ord('q') or key == ord('Q') or key == 27:  # Q或ESC退出
            break
    
    # 5. 清理
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n程序已退出，共拍摄 {photo_count} 张照片")

if __name__ == "__main__":
    main()