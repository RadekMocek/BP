# Soustavy lineárnı́ch rovnic

* Zdroje:
  * [RNDr. Zdeněk Kalousek CSc.](https://kma.fp.tul.cz/?view=article&id=600&catid=147)
    * 3\. přednáška z lineární algebry: Soustavy rovnic o _n_ neznámých a jejich řešení Gaussovou eliminací

## Rovnice s _n_ neznámými

* _f(x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>n</sub>)_ = _b_
* Požadujeme, aby funkce _f_ náležela do vektorového prostoru _V<sub>D</sub>_ (nad _T_) funkcí definovaných na množině _D_, ve kterém jsou standardně definované operace pro všechny _n_-tice (x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>n</sub>) z _D_:
  * (_f_ ⊕ _g_)(_x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>n</sub>_) = _f(x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>n</sub>)_ + _g(x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>n</sub>)_
  * (_α_ ⊗ _f_)(_x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>n</sub>_) = _α_ ⋅ _f(x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>n</sub>)_
* Pro rovnice můžeme zavést sčítání a násobení číslem z _T_
  * _r_ = (_f(x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>n</sub>)_ = _b_)
  * _s_ = (_g(x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>n</sub>)_ = _d_)
  * _r_ ⊕ _s_ = (_f(x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>n</sub>)_ + _g(x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>n</sub>)_ = _b_ + _d_)
  * _α_ ⊗ _r_ = (_α_ ⋅ _f(x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>n</sub>)_ = _α_ ⋅ _b_)
* Množina rovnic o _n_ neznámých s funkcemi z prostoru _V<sub>D</sub>_ a takto definovanými operacemi tvoří vektorový prostor

## Soustava rovnic

* Konečnou množinu rovnic _R_ = {_r<sub>1</sub>, r<sub>2</sub>, ..., r<sub>m</sub>_}, kde _r<sub>i</sub>_ = (_f<sub>i</sub>(x<sub>1</sub>, x<sub>2</sub>, ..., x<sub>n</sub>) = b<sub>i</sub>_) nazveme soustava rovnic o _n_ neznámých
* Řešením soustavy je každá _n_-tice, která je řešením všech rovnic soustavy
* Pokud je _n_-tice řešením soustavy rovnic _R_, pak je i řešením jakékoliv lineární kombinace rovnic z _R_
* Jsou-li _R_ a _S_ soustavy rovnic o _n_ neznámých pro funkce z prostoru _V<sub>D</sub>_ a span(_R_) = span(_S_), pak mají stejnou množinu řešení

## Lineární rovnice s _n_ neznámými

* _a<sub>1</sub> x<sub>1</sub>_ + _a<sub>2</sub> x<sub>2</sub>_ + ... _a<sub>n</sub> x<sub>n</sub>_ = _b_
  * _a<sub>j</sub>_ → koeficienty rovnice
  * _x<sub>j</sub>_ → neznámé v rovnici
  * _b_ → pravá strana rovnice
  * Na levé straně rovnice se nacházejí ryze lineární funkce _n_ proměnných
  * Zkráceně:

$$$render
\sum_{j=1}^na_jx_j=b
$$

## Izomorfismus

* Jsou-li _U_=(_M_, ⊕<sub>u</sub>, ⊗<sub>u</sub>) a _V_=(_N_, ⊕<sub>v</sub>, ⊗<sub>v</sub>) vektorové prostory nad stejným číselným tělesem a existuje prosté zobrazení _I_ množiny _M_ na množinu _N_ [_D(I)_=_M_ a _W(I)_=_N_], kde platí:
  * _I_(_a_ ⊕<sub>u</sub> _b_) = _I_(_a_) ⊕<sub>v</sub> _I_(_b_)
  * _I_(_α_ ⊗<sub>u</sub> _a_) = _α_ ⊗<sub>v</sub> _I_(_a_)
* pak řekneme, že prostory _U_ a _V_ jsou izomorfní a zobrazení _I_ je jejich izomorfismem.
* Podstatou je, že nezáleží na tom, ve kterém z prostorů operace provádíme
  * Můžeme úlohu "přeložit" z jednoho prostoru do druhého (kde se nám lépe pracuje) a poté provést "zpětný překlad"
* Zobrazení, které rovnici _a<sub>1</sub> x<sub>1</sub>_ + _a<sub>2</sub> x<sub>2</sub>_ + ... _a<sub>n</sub> x<sub>n</sub>_ = _b_ přiřadí (_n_+1)-tici čísel (_a<sub>1</sub>_ + _a<sub>2</sub>_ + ... _a<sub>n</sub>_, _b_) je izomorfismem prostoru lineárních rovnic o _n_ neznámých s prostorem _T_<sup>n+1</sup>

## Řešení soustav pomocí Gaussovy eliminace

* Soustavu rovnic tedy můžeme "přeložit" na soustavu (_n_+1)-tic a s nimi provádět gaussovské operace (které nezmění lineární obal)
* (_n_+1)-tice upravíme do příjemnější podoby, jelikož se lineární obal nezměnil, upravená (_n_+1)-tice má stejnou množinu řešení jako původní (_n_+1)-tice
* Soustavy se řeší vepsáním (_n_+1)-tic do matice
