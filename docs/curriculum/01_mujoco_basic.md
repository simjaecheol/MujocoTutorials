# 01. MuJoCo 기초 및 물리 시뮬레이션 입문

> **실습 노트북 바로가기**: [Notebook 01: `01_mujoco_basic.ipynb` 웹에서 보기](../notebooks/01_mujoco_basic.ipynb)

![Dominoes Demo](../assets/imgs/dominoes.gif)

---

## 학습 목표
1. **MJCF(XML) 모델링 문법**: `<mujoco>`, `<worldbody>`, `<body>`, `<geom>`, `<joint>`의 계층 구조와 기본값 규칙 이해
2. **`mjModel` vs `mjData` 분리 아키텍처**:
   * `mjModel`: 시간이 지나도 변하지 않는 정적 모델 구조 및 물리 파라미터 (`ngeom`, `nv`, `opt.timestep`, `opt.gravity`)
   * `mjData`: 매 타임스텝마다 변하는 시뮬레이션 상태 (`time`, `qpos`, `qvel`) 및 파생 물리량 (`geom_xpos`, `contact`, `sensordata`)
3. **일반화 좌표계 (Generalized Coordinates)**:
   * 왜 `mj_kinematics` 또는 `mj_forward`를 호출해야 전역 직교 좌표(`xpos`)가 갱신되는가?
   * 6자유도 자유 물체(`<freejoint/>`)의 위치 벡터(`qpos`, 길이 7: 3D 위치 + 4D 단위 쿼터니언)와 속도 벡터(`qvel`, 길이 6: 3D 선속도 + 3D 각속도)의 차이
4. **수치 적분과 카오스 동역학**:
   * 뒤집히는 팽이(Tippe-Top)에서의 4차 룽게-쿠타(`RK4`) 적분기 활용
   * 카오스 진자(Chaotic Pendulum)에서의 초기 조건 민감도($10^{-7}$ 섭동) 및 타임스텝(`timestep`) 크기에 따른 에너지 보존·수치 발산 분석
5. **접촉·마찰·센서·고급 렌더링**:
   * 접촉점/접촉력 벡터 시각화 및 `mj_contactForce` 계측
   * 힘줄(`<tendon>`), 모터(`<actuator>`), 가속도계 센서(`<accelerometer>`)
   * 깊이(Depth) 및 세그멘테이션(Segmentation) 렌더링, $3 \times 4$ 카메라 행렬을 이용한 3D → 2D 픽셀 투영, 도미노 시뮬레이션

---

## 핵심 코드 요약

```python
import mujoco
import mediapy as media
from utils.notebook_setup import init_notebook

init_notebook()

xml = """
<mujoco>
  <worldbody>
    <light name="top" pos="0 0 1"/>
    <body name="box_and_sphere" euler="0 0 -30">
      <joint name="swing" type="hinge" axis="1 -1 0" pos="-.2 -.2 -.2"/>
      <geom name="red_box" type="box" size=".2 .2 .2" rgba="1 0 0 1"/>
      <geom name="green_sphere" pos=".2 .2 .2" size=".1" rgba="0 1 0 1"/>
    </body>
  </worldbody>
</mujoco>
"""
model = mujoco.MjModel.from_xml_string(xml)
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model)

frames = []
mujoco.mj_resetData(model, data)
while data.time < 3.8:
    mujoco.mj_step(model, data)
    if len(frames) < data.time * 60:
        renderer.update_scene(data)
        frames.append(renderer.render())

media.show_video(frames, fps=60)
```

