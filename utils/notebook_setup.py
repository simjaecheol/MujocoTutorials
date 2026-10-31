"""
Windows 환경을 위한 Jupyter Notebook 공통 초기화 유틸리티.
- mediapy에서 내장 ffmpeg(imageio-ffmpeg)를 자동으로 사용하도록 연결합니다.
- matplotlib 한글 폰트(맑은 고딕) 및 마이너스 기호 깨짐을 방지합니다.
- 프로젝트 루트 디렉토리를 기준으로 상대 경로(robot/ 등)가 항상 동작하도록 보장합니다.
"""
import os
import platform
from pathlib import Path
import matplotlib.pyplot as plt


def init_notebook():
    """노트북 실행 환경을 초기화합니다."""
    # 1. imageio-ffmpeg를 통해 mediapy에 ffmpeg 실행 파일 경로 자동 등록
    try:
        import imageio_ffmpeg
        import mediapy as media
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        media.set_ffmpeg(ffmpeg_path)
    except Exception as e:
        print(f"[경고] ffmpeg 자동 설정 중 문제가 발생했습니다: {e}")

    # 2. Windows 한글 폰트 설정 (matplotlib)
    if platform.system() == "Windows":
        plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

    # 3. 작업 디렉토리를 프로젝트 루트로 맞춤
    cwd = Path.cwd()
    if not (cwd / "robot").exists() and (cwd.parent / "robot").exists():
        os.chdir(cwd.parent)

    print(f"환경 초기화 완료 (현재 작업 경로: {Path.cwd()})")

