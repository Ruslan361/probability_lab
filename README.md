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