# Čı́selné matice a operace s nimi

## Násobení matic

* Matici <i>m<sub>1</sub></i>×<i>n<sub>1</sub></i> můžeme vynásobit maticí <i>m<sub>2</sub></i>×<i>n<sub>2</sub></i>, pokud <i>n<sub>1</sub></i> = <i>m<sub>2</sub></i>
  * Rozměr výsledné matice je pak <i>m<sub>1</sub></i>×<i>n<sub>2</sub></i>
* Násobení matic není komutativní
* Násobení matic je asociativní

$$$render
[1,2;3,4]\cdot[5,6;7,8]=[1\cdot5+2\cdot7,1\cdot6+2\cdot8;3\cdot5+4\cdot7,3\cdot6+4\cdot8]=[19,22;43,50]
$$

* Prvek v _i_-tém řádku a _j_-tém sloupci lze chápat jako součet součinů prvků _i_-tého řádku první matice s _j_-tým sloupcem druhé matice

$$$render
c_{ij}=\sum_{k=1}^na_{ik}b_{kj}
$$

## Matice přechodu

* Sloupce matice _P<sub>E→F</sub>_ jsou tvořeny souřadnicovými vektory vektorů baze _E_ v bazi _F_
* Vynásobením matice přechodu _P<sub>E→F</sub>_ vektorem se souřadnicemi v bazi _E_ dostaneme jeho souřadnice v bazi _F_
* _P<sub>E→G</sub>_ = _P<sub>F→G</sub>_ ⋅ _P<sub>E→F</sub>_
  * Jedeme zprava doleva

### Konstrukce matice přechodu

* ( _Y_ | _X_ ) ~ ( _E_ | _P<sub>X→Y</sub>_ ) ~ ( _P<sub>Y→X</sub>_ | _E_ )
* Do levé části matice vepíšeme (po sloupcích, ve správném pořadí) vektory cílové baze a do pravé části vektory startovní baze
  * Po použití Gaussovy-Jordanovy eliminační metody nám vlevo vyjde jednotková matice a vpravo vyjde matice přechodu
* Pro matici přechodu z baze do kanonické baze stačí vepsat bazové vektory (nekanonické) baze po sloupcích do matice

## Matice reprezentující gaussovské operace

* Gaussovské operace s řádky matice se dají chápat jako násobení eliminované matice speciální "gaussovskou" maticí _G_ **zleva**

1. Výměna řádků _i_, _j_
    * Matice _G_ je stejná jako jednotková matice, jen má prohozené řádky _i_ a _j_
    * _g<sub>ij</sub>_ = _g<sub>ji</sub>_ = 1
    * _g<sub>kk</sub>_ = 1 pro všechna _k_ kromě _k_ = _i_ a _k_ = _j_
2. Vynásobení _i_-tého řádku číslem _α_
    * Matice _G_ je stejná jako jednotková matice, na řádku _i_ je ale místo jedničky číslo _α_
    * _g<sub>kk</sub>_ = 1 pro všechna _k_ kromě _k_ = _i_
    * _g<sub>ii</sub>_ = _α_
3. Přičtení _α_-násobku _i_-tého řádku k _j_-tému řádku
    * _g<sub>ji</sub>_ = _α_
    * _g<sub>kk</sub>_ = 1
4. Vynechání _i_-tého řádku
    * _G_ je matice s _n_-1 řádky a _n_ sloupci
    * _g<sub>k,k</sub>_ = 1 pro všechna _k_ < _i_
    * _g<sub>k,k+1</sub>_ = 1 pro všechna _k_ ≥ _i_

## Jednotková matice

* Existuje právě jedna
* Na diagonále má jedničky a všude jinde nuly

## Inverzní matice

* Máme matici přechodu _P<sub>E→F</sub>_ a chceme znát také matici opačného přechodu _P<sub>F→E</sub>_
  * Cílem je vytvořit matici _P<sub>F→E</sub>_, která po vynásobení (zleva i zprava) původní maticí _P<sub>E→F</sub>_ dá jednotkovou matici
  * Říkáme, že matice _P<sub>F→E</sub>_ je inverzní k matici _P<sub>E→F</sub>_
  * Píšeme _P<sub>F→E</sub>_ = (_P<sub>E→F</sub>_)<sup>-1</sup>
* K regulárním maticím lze vytvořit inverzní matici (k singulárním nikoliv)

### Výpočet inverzní matice

* Do levé části napíšeme původní matici, do pravé jednotkovou matici; v levé části provedeme Gaussovu-Jordanovu eliminaci a vpravo nám vyjde inverzní matice
* S jednotkovou maticí provádíme stejné řádkové operace, které provádíme při transformaci původní matice na jednotkovou
* Nejdříve dostaneme matici do horního stupňovitého tvaru, poté vytvoříme diagonální matici nulováním naddiagonální části, kdykoliv v průběhu eliminace násobíme "diagonální řádky" potřebnými koeficienty pro vznik "jednotkových řádků"

## Matice jako uspořádaná sada čísel

* Číselná matice <i>m</i>×<i>n</i> je uspořádanou _mn_-ticí čísel, lze ji považovat za vektor z _T<sup>mxn</sup>_
* Součet matic _A_ a _B_ o rozměrech <i>m</i>×<i>n</i> je matice _C_ = _A_ + _B_, která má také rozměr <i>m</i>×<i>n</i> a platí _c<sub>ij</sub>_ = _a<sub>ij</sub>_ + _b<sub>ij</sub>_
* _α_-násobkem matice _A_ je matice _C_ = _αA_ o stejných rozměrech, kde platí _c<sub>ij</sub>_ = _α_ ⋅ _a<sub>ij</sub>_
* Tímto způsobem můžeme zavést i lineární kombinaci matic
* Kromě toho, že násobení matic není komutativní, můžeme s maticemi při kombinování sčítání a násobení (další maticí nebo číslem) zacházet stejně jako s čísly

## Transpozice matice

* Vzájemná výměna řádků a sloupců

## Bloková matice

* Matici můžeme vodorovnými a svislými čarami rozdělit na části nazývané bloky, což jsou opět matice obecně menších rozměrů
* Bloková matice je matice _A_ <i>m</i>×<i>n</i>, jejímiž prvky jsou matice _A<sub>ij</sub>_ navzájem kompatibilních rozměrů <i>r<sub>i</sub></i>×<i>s<sub>j</sub></i>
* Na blokové matice lze pohlížet jako na běžné matice
* Jsou-li ovšem sčítané/násobené matice rozděleny do bloků "sobě odpovídajícím způsobem", pak jejich součet/násobek lze opět zapsat jako blokovou matici a operace sčítání/násobení je možné provádět po blocích
