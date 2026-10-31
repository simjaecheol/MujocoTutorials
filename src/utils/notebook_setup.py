"""
Windows 환경을 위한 Jupyter Notebook 공통 초기화 및 에셋 경로 유틸리티.
- mediapy에서 내장 ffmpeg(imageio-ffmpeg)를 자동으로 사용하도록 연결합니다.
- matplotlib 한글 폰트(맑은 고딕) 및 마이너스 기호 깨짐을 방지합니다.
- notebooks/ 하위에서 실행하더라도 프로젝트 루트 디렉토리를 작업 경로로 자동 설정합니다.
- 튜토리얼 전용 로봇 설정(assets/robots/), MuJoCo Menagerie 서브모듈(assets/mujoco_menagerie/),
  그리고 3D 물체 에셋(assets/objects/) 경로 헬퍼를 제공합니다.
"""
import os
import platform
import sys
from pathlib import Path
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
ROBOTS_DIR = ASSETS_DIR / "robots"
MENAGERIE_DIR = ASSETS_DIR / "mujoco_menagerie"
OBJECTS_DIR = ASSETS_DIR / "objects"
IMGS_DIR = ASSETS_DIR / "imgs"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"


def list_menagerie_robots() -> list[str]:
    """assets/mujoco_menagerie 서브모듈 내의 사용 가능한 모든 로봇 모델 디렉토리 목록을 반환합니다."""
    if not MENAGERIE_DIR.exists():
        return []
    return sorted([
        d.name for d in MENAGERIE_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".") and any(d.glob("scene*.xml"))
    ])


def get_robot_scene_path(robot_name: str, use_menagerie: bool = False) -> str:
    """
    로봇 이름에 해당하는 MJCF scene XML 경로를 반환합니다.
    - 기본 튜토리얼 로봇('ur5e', 'panda', 'kuka', 'aloha'): 모캡 타겟/토크 액추에이터/PBR이 설정된 assets/robots/ 내 XML 반환
      (3D 메쉬는 assets/mujoco_menagerie 서브모듈을 공유)
    - use_menagerie=True 이거나 그 외 60+종 로봇 이름('unitree_go1', 'unitree_g1', 'leap_hand', 'shadow_hand' 등):
      assets/mujoco_menagerie/<robot_name>/scene*.xml 반환
    """
    tutorial_mapping = {
        "ur5e": ROBOTS_DIR / "universal_robots_ur5e" / "scene.xml",
        "universal_robots_ur5e": ROBOTS_DIR / "universal_robots_ur5e" / "scene.xml",
        "panda": ROBOTS_DIR / "franka_emika_panda" / "scene.xml",
        "franka_emika_panda": ROBOTS_DIR / "franka_emika_panda" / "scene.xml",
        "kuka": ROBOTS_DIR / "kuka_iiwa_14" / "scene.xml",
        "kuka_iiwa_14": ROBOTS_DIR / "kuka_iiwa_14" / "scene.xml",
        "aloha": ROBOTS_DIR / "aloha" / "scene_pbr.xml",
    }
    menagerie_aliases = {
        "ur5e": "universal_robots_ur5e",
        "panda": "franka_emika_panda",
        "kuka": "kuka_iiwa_14",
        "go1": "unitree_go1",
        "go2": "unitree_go2",
        "g1": "unitree_g1",
        "h1": "unitree_h1",
        "spot": "boston_dynamics_spot",
    }
    key = robot_name.lower()
    if not use_menagerie and key in tutorial_mapping:
        return str(tutorial_mapping[key])

    menagerie_name = menagerie_aliases.get(key, key)
    robot_dir = MENAGERIE_DIR / menagerie_name
    if robot_dir.exists():
        for candidate in ["scene.xml", "scene_right.xml", "scene_position.xml"]:
            if (robot_dir / candidate).exists():
                return str(robot_dir / candidate)
        scenes = sorted(robot_dir.glob("scene*.xml"))
        if scenes:
            return str(scenes[0])

    raise ValueError(
        f"알 수 없는 로봇 이름입니다: {robot_name}. "
        f"튜토리얼 기본: {list(tutorial_mapping.keys())}, "
        f"Menagerie 지원({len(list_menagerie_robots())}종): list_menagerie_robots()로 확인하세요."
    )


def init_notebook() -> Path:
    """노트북 실행 환경을 초기화하고 프로젝트 루트 경로(Path)를 반환합니다."""
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

    # 3. 작업 디렉토리를 프로젝트 루트로 맞춤 (notebooks/ 폴더 안에서 실행될 때 상위 루트로 이동)
    cwd = Path.cwd()
    if (cwd / "assets").exists():
        project_root = cwd
    elif (cwd.parent / "assets").exists():
        project_root = cwd.parent
        os.chdir(project_root)
    else:
        project_root = PROJECT_ROOT
        if (project_root / "assets").exists():
            os.chdir(project_root)

    # 4. src 폴더가 sys.path에 없으면 추가
    src_dir = str(project_root / "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    print(f"환경 초기화 완료 (프로젝트 루트: {project_root})")
    return project_root
