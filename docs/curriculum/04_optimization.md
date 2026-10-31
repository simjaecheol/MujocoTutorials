# 04. 로보틱스를 위한 비볼록 수치 최적화 (Nonconvex Optimization)

> **실습 노트북 바로가기**: [Notebook 04: `04_optimization.ipynb` 웹에서 보기](../notebooks/04_optimization.ipynb)

![Augmented Lagrangian](../assets/imgs/augmented_lagrangian.png)

---

## 학습 목표
1. **무제약 비볼록 최적화와 레벤버그-마쿼트(Levenberg-Marquardt) 정규화**:
   * 비볼록 함수에서 헤시안 $H_k$가 양의 정부호(SPD)가 아닐 때 발생하는 문제를 신뢰 영역 정규화 $(H_k + \mu I)$로 해결:
     $$x_{k+1} = x_k - (H_k + \mu I)^{-1} g_k$$
2. **비선형 최소제곱법과 가우스-뉴턴(Gauss-Newton) 근사법**:
   * 목적 함수 $f(x) = \frac{1}{2}\|r(x)\|_2^2$에서 2차 미분 없이 자코비안 $J = \nabla r(x)$만으로 헤시안을 $H_{GN} = J^T J$로 근사하는 원리
   * 로젠브록(Rosenbrock) 및 빌(Beale) 벤치마크 함수에서 경사하강법, 완전 뉴턴법, 가우스-뉴턴법, 그리고 `mujoco.minimize.least_squares`의 수렴 궤적 비교
3. **등식 제약 조건부 최적화 ($\min_x f(x) \ \text{s.t.} \ g(x) = 0$)**:
   * **페널티 방법 (Penalty Method)**: $\rho \to \infty$ 증가에 따른 지형 변화와 조건수(Ill-conditioning) 한계
   * **원시-쌍대 방법 (Primal-Dual Method)**: 라그랑지안 $\mathcal{L}(x, \lambda) = f(x) + \lambda^T g(x)$의 KKT 조건에 대한 뉴턴-랩슨 동시 해법
   * **증강 라그랑지안 방법 (Augmented Lagrangian Method, ALM)**:
     $$\mathcal{L}_\rho(x, \lambda) = f(x) + \lambda^T g(x) + \frac{\rho}{2}\|g(x)\|_2^2$$
     최소제곱 서브루틴 풀이와 쌍대 변수 업데이트($\lambda_{k+1} = \lambda_k + \rho_k g(x_{k+1})$)를 통한 안정적이고 빠른 수렴 확인

