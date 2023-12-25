# Ortogonalizace

V lineárním obalu množiny vektorů
    _G_ = { _g<sub>1</sub>_ = (1,1,1,1), _g<sub>2</sub>_ = (5,1,-2,0), _g<sub>3</sub>_ = (1,3,-1,1) }
vytvořte ortogonální množinu.

* První vektor zařadíme rovnou, zatím tedy _F_ = { _f<sub>1</sub>_ = (1,1,1,1) }
* Další vektory musíme upravit následujícím způsobem

$$$render
\tilde{f}_{n+1}=g\bigoplus_{i=1}^{n}\left(-\frac{\langle f_i|g\rangle}{\|f_i\|^2}\otimes f_i\right)
$$

* Vezmeme další vektor z _G_ a odečteme od něj určité násobky všech již ortogonálních vektorů z _F_
* Určitým násobkem je zlomek
  * V čitateli je skalární součin ortogonálního vektoru s vektorem, který chceme přidat ⟨_f<sub>i</sub>_|_g_⟩
  * Ve jmenovateli je norma na druhou ortogonálního vektoru
* Výsledný vektor přidáme do _F_, tyto kroky opakujeme, dokud nevyčerpáme _G_

$$$render
\tilde{f}_{n+1}=(5,1,-2,0)-\frac{\langle(1,1,1,1)|(5,1,-2,0)\rangle}{\|(1,1,1,1)\|^2}\cdot(1,1,1,1)=(5,1,-2,0)-\frac{4}{4}\cdot(1,1,1,1)=(4,0,-3,-1)
$$

* Nyní _F_ = { _f<sub>1</sub>_ = (1,1,1,1), _f<sub>2</sub>_ = (4,0,-3,-1) }, zpracujeme poslední vektor z _G_

$$$render
\tilde{f}_{n+1}=(1,3,-1,1)-\frac{\langle(1,1,1,1)|(1,3,-1,1)\rangle}{\|(1,1,1,1)\|^2}\cdot(1,1,1,1)-\frac{\langle(4,0,-3,-1)|(1,3,-1,1)\rangle}{\|(4,0,-3,-1)\|^2}\cdot(4,0,-3,-1)\\
\tilde{f}_{n+1}=(1,3,-1,1)-\frac{4}{4}\cdot(1,1,1,1)-\frac{6}{26}\cdot(4,0,-3,-1)=\left(-\frac{12}{13},2,-\frac{17}{13},\frac{3}{13}\right)
$$

* Výsledná množina je _F_ = { _f<sub>1</sub>_ = (1,1,1,1), _f<sub>2</sub>_ = (4,0,-3,-1), _f<sub>3</sub>_ = (-12/13, 2, -17/13, 3/13) }
