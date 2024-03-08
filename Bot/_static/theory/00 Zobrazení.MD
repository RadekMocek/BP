# Zobrazení

* Zdroje:
  * [RNDr. Zdeněk Kalousek CSc.](https://kma.fp.tul.cz/?view=article&id=600&catid=147)
    * Vstupní přednáška z Úvodu do lineární algebry a DM: Zobrazení

## Definice zobrazení

* Zobrazení _f_ z množiny _M_ do množiny _N_ je předpis, který každému prvku _m_ ∈ _M_ (vzor) přiřazuje nejvýše jeden prvek _n_ ∈ _N_ (obraz)
* Je-li prvku _m_ ∈ _M_ přiřazen prvek _n_ ∈ _N_, nazýváme _n_ obrazem prvku _m_ při zobrazení _f_
  * Píšeme _n = f(m)_ a říkáme "_n_ je obraz prvku _m_"
* Vztah se také zachycuje zápisem _f_ : _M_ → _N_

### Příklad zobrazení

* _M_ je množina dvojic přirozených čísel a součet prvků je zobrazení, které dvojici _m_ = (_m<sub>1</sub>_, _m<sub>2</sub>_) přířadí přirozené číslo _f(m)_ =  _m<sub>1</sub>_ + _m<sub>2</sub>_; pro každý vzor existuje právě jeden obraz
* _M_ je množina dvojic přirozených čísel doplněných o nulu a podíl se zbytkem je zobrazení, které dvojici _m_ = (_m<sub>1</sub>_, _m<sub>2</sub>_) přířadí dvojici _n_ = (_n<sub>1</sub>_, _n<sub>2</sub>_) takovou, že _m<sub>1</sub>_ = _n<sub>1</sub>_ ⋅ _m<sub>2</sub>_ + _n<sub>2</sub>_; pro každý vzor existuje právě jeden obraz s výjimkou, kdy _m<sub>2</sub>_ = 0

## Definiční obor

* Ne každému vzoru je při obecném zobrazení přiřazen jeho obraz
  * Zavedena množina všech vzorů, pro které má smysl obrazy hledat
* Definiční obor zobrazení _f_ je taková podmožina _D(f)_ množiny _M_, kde pro každé _d_ ∈ _D(f)_ existuje obraz _f(d)_ ∈ _N_
  * Pro prvky množiny _M_, které nenáležejí _D(f)_, obraz neexistuje
* Je-li definičním oborem zobrazení celá množina _M_, mluvíme o "zobrazení množiny _M_" (vynecháme předložku "z")
  * Zobrazení _f_ ~~z~~ množiny _M_ do množiny _N_

## Obor hodnot

* Obor hodnot zobrazení _f_ je taková podmnožina _W(f)_ množiny _N_, kde pro každé _w_ ∈ _W(f)_ existuje takový prvek _m_ ∈ _M_, že _f(m)_ = _w_
* "Množina všech obrazů (prvků cílové množiny _N_), jejichž vzor je neprázdný."
* Je-li oborem hodnot zobrazení celá množina _N_, mluvíme o "zobrazení na množinu _N_" (namísto "do množiny _N_")

## Vzor prvku oboru hodnot

* Může se stát, že se více vzorů zobrazí do téhož obrazu (5+2=7 a 3+4=7)
* Vzorem prvku _n_ ∈ _N_ je množina _f_ <sup>(-1)</sup>(_n_)
  * Do této množiny patří všechny prvky z množiny _M_, pro které platí _f(m) = n_
  * Vzor prvku se dá považovat za zobrazení _f_ <sup>(-1)</sup> : _N_ → _množina všech podmnožin množiny M_ (značíme 2<sup>M</sup>)

## Prosté zobrazení

* Vzorem každého prvku cílové množiny _N_ je nejvýše jednoprvková množina
  * Ke každému obrazu je přiřazen nejvýše jeden vzor
* Zobrazení _f_ : _M_ → _N_ je prosté, pokud pro každé dva prvky _m<sub>1</sub>_ ≠ _m<sub>2</sub>_ z _D(f)_ platí, že _f(m<sub>1</sub>)_ ≠ _f(m<sub>2</sub>)_

## Inverzní zobrazení

* Je-li zobrazení _f_ : _M_ → _N_ prosté, pak zobrazení, které každému prvku _w_ ∈ _W(f)_ přiřazuje prvek _m_ ∈ _M_, kde platí _w_ = _f(m)_, nazveme zobrazením inverzním k _f_
  * Značíme ho jako _f_ <sup>-1</sup> a píšeme _m_ = _f_ <sup>-1</sup>(_w_)
* Poté platí následující tvrzení:
  1. Je-li _f_ : _M_ → _N_, pak _f_ <sup>-1</sup> : _N_ → _M_
  2. _D(f <sup>-1</sup>)_ = _W(f)_
  3. _W(f <sup>-1</sup>)_ = _D(f)_

## Skládání zobrazení

* Máme-li zobrazení _f_ : _M_ → _N_ a _g_ : _N_ → _O_, pak existuje zobrazení _h_ : _M_ → _O_ složené ze zobrazení _f_ a _g_
  * Platí _h(m)_ = _g(f(m))_
  * Zapisujeme ve tvaru _h_ = _g(f)_ nebo _h_ = _g_ ◦ _f_

## Identita

* _i<sub>M</sub>_ (identické zobrazení na _M_) každému prvku _m_ přiřadí znovu tento prvek
  * _i<sub>M</sub> : M → M_
  * _i<sub>M</sub>(m) = m_
* Při skládání zobrazení hraje identické zobrazení roli neutrálního prvku
  * Pro _f_ : _M_ → _N_ je _f_ to samé jako *i<sub>N</sub>*(*f*(_i<sub>M</sub>_))
* Je-li _f_ : _M_ → _N_ prosté, pak
  * _f_ <sup>-1</sup>(_f_) = _i<sub>D(f)</sub>_
  * *f*(_f_ <sup>-1</sup>) = _i<sub>W(f)</sub>_
