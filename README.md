# Лабораторная работа №2

## Экспоненциальное распределение со сдвигом

Экспоненциальное распределение со сдвигом определяется плотностью вероятности:

$$f(x) = \begin{cases}
\lambda e^{-\lambda(x - \theta)}, & x \ge \theta\\
0, & x < \theta
\end{cases}$$

где $\lambda > 0$ — параметр скорости (rate parameter), а $\theta$ — параметр сдвига.

### Вывод матожидания:

Матожидание (M[X]) случайной величины X с экспоненциальным распределением со сдвигом вычисляется следующим образом:

$M[X] = \int_{\theta}^{\infty} x f(x) dx = \int_{\theta}^{\infty} x \lambda e^{-\lambda(x - \theta)} dx$

Для упрощения интегрирования сделаем замену переменной:  $u = x - \theta$, $du = dx$, $x = u + \theta$. Пределы интегрирования меняются: $x = \theta \Rightarrow u = 0$, $x = \infty \Rightarrow u = \infty$.

$M[X] = \int_{0}^{\infty} (u + \theta) \lambda e^{-\lambda u} du = \int_{0}^{\infty} u \lambda e^{-\lambda u} du + \theta \int_{0}^{\infty} \lambda e^{-\lambda u} du$

Первый интеграл представляет собой матожидание стандартного экспоненциального распределения (без сдвига) с параметром $\lambda$, которое равно $\frac{1}{\lambda}$. Второй интеграл — это интеграл от плотности вероятности стандартного экспоненциального распределения, который равен 1.

$M[X] = \frac{1}{\lambda} + \theta \cdot 1 = \theta + \frac{1}{\lambda}$

### Вывод дисперсии:

Дисперсия $\sigma^2$ вычисляется как $\sigma^2[X] = M[X^2] - (M[X])^2$. Сначала найдем $M[X^2]$:

$M[X^2] = \int_{\theta}^{\infty} x^2 f(x) dx = \int_{\theta}^{\infty} x^2 \lambda e^{-\lambda(x - \theta)} dx$

Снова используем замену $u = x - \theta$:

$M[X^2] = \int_{0}^{\infty} (u + \theta)^2 \lambda e^{-\lambda u} du = \int_{0}^{\infty} (u^2 + 2u\theta + \theta^2) \lambda e^{-\lambda u} du$

$M[X^2] = \int_{0}^{\infty} u^2 \lambda e^{-\lambda u} du + 2\theta \int_{0}^{\infty} u \lambda e^{-\lambda u} du + \theta^2 \int_{0}^{\infty} \lambda e^{-\lambda u} du$

Первый интеграл — это второй момент стандартного экспоненциального распределения, равный $\frac{2}{\lambda^2}$. Второй интеграл — это матожидание стандартного экспоненциального распределения, равное $\frac{1}{\lambda}$. Третий интеграл равен 1.

$M[X^2] = \frac{2}{\lambda^2} + 2\theta \frac{1}{\lambda} + \theta^2$

Теперь вычислим дисперсию:

$\sigma^2[X] = M[X^2] - (M[X])^2 = \frac{2}{\lambda^2} + \frac{2\theta}{\lambda} + \theta^2 - \left(\theta + \frac{1}{\lambda}\right)^2 = \frac{2}{\lambda^2} + \frac{2\theta}{\lambda} + \theta^2 - \left(\theta^2 + \frac{2\theta}{\lambda} + \frac{1}{\lambda^2}\right) = \frac{1}{\lambda^2}$

* Матожидание экспоненциального распределения со сдвигом: $M[X] = \theta + \frac{1}{\lambda}$
* Дисперсия экспоненциального распределения со сдвигом: $\sigma^2[X] = \frac{1}{\lambda^2}$
* Квантильная функция (обратная функция распределения): $F^{-1}(p) = \theta - \frac{ln(1 - p)}{\lambda}, \quad 0 \le p < 1$


## Треугольное распределение
### Функции плотности вероятности:


$$f(x) = \begin{cases}
b + k \left(- \phi + x\right), & x \in [\phi - \frac{b}{k}, \phi]\\
 b - k \left(- \phi + x\right), & x \in (\phi, \phi + \frac{b}{k}]
\\
0, & x \notin [\phi - \frac{b}{k}, \phi + \frac{b}{k}]
\end{cases}$$



### Проверка условий нормировки:
 Чтобы выполнялись условия нормировки необходимо, чтобы
 $b = \sqrt{k}$

 Таким образом, 

$$f(x) = \begin{cases}
\sqrt{k} - k \left(\phi - x\right), & x \in [\phi - \frac{1}{\sqrt{k}}, \phi]\\
 \sqrt{k} + k \left(\phi - x\right), & x \in \left(\phi, \phi + \frac{1}{\sqrt{k}}\right]
\\
0, & x \notin \left[\phi - \frac{b}{k}, \phi + \frac{b}{k}\right]
\end{cases}$$


### Функция распределения:

 $$F(x) = \begin{cases}
 0, & x \in (-\infty,  \phi - \frac{1}{\sqrt{k}})
 \\
\frac{\phi^{2} k}{2} - \phi \sqrt{k} - \phi k x + \sqrt{k} x + \frac{k x^{2}}{2} + \frac{1}{2}, & x \in [\phi - \frac{1}{\sqrt{k}}, \phi]\\
 -\frac{\phi^{2} k}{2} - \phi \sqrt{k} + \phi k x + \sqrt{k} x - \frac{k x^{2}}{2} + \frac{1}{2}, & x \in (\phi, \phi + \frac{1}{\sqrt{k}}]
\\
1, & x \in (\phi + \frac{b}{k},  +\infty)
\end{cases}$$


### Математическое ожидание:

 $M(X) = \phi$

### Дисперсия:

 $D(X) = \frac{1}{6 k}$

### Обратная функция:

При $0 < y \le \frac{1}{2}$

$x = \frac{\phi\sqrt{k} - \sqrt{2y} - 1}{\sqrt{k}}$ или

$x = \frac{\phi\sqrt{k} + \sqrt{2y} - 1}{\sqrt{k}}$ и

$x \in [\phi - \frac{1}{\sqrt{k}}, \phi]$ 
При $\frac{1}{2} < F(x) \le 1$

$x = \frac{\phi k + \sqrt{k} - \sqrt{2k(1-y)}}{k}$ или

$x = \frac{\phi k + \sqrt{k} + \sqrt{2k(1-y)}}{k}$ и

$x \in \left(\phi, \phi + \frac{1}{\sqrt{k}}\right]$


