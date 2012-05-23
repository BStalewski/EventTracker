Cześć,

niestety, zawiodłem:( Zabrakło mi czasu. Algorytm wygląda następująco.
Wszystko opiera się na obiektach opisujących pola, które mogą wystąpić w filmie:
- key - nazwa pola, np. Reżyseria(to podaje się przy przekazywaniu stron)
- path - ścieżka do tego elementu, przy czym w tej ścieżce pomijane są elementy puste, więc nie ma znaczenia ile jest brów itp.
- keyVisible - czy nazwa z key występuje na stronie
- long - czy zawartością pola jest jakiś dłuższy tekst (zdanie/zdania)
- multiple - czy może być dużo wartości (np. kilku scenarzystów), jeśli to pole jest prawdziwe, to dodawane jest także pole "sep" mówiące co oddziela wartości w tym polu

Takie pola powstają po opisie jednej strony. Użytkownik podaje tylko pola "key" i "value"(czyli co na danej stronie znajduje się w tym polu). Program znajduje elementy zawierające value. Może być ich dużo na stronie. Jak znajdowane są ścieżki do elementów: dla pierwszego typu elementów, np. (Reżyser) wyszukiwane są na stronie elementy zawierające wartość tego pola. Może być ich dużo, dlatego tworzona jest lista. Potem dla każdego następnego elementu także wyszukiwane są ścieżki i znajdowane są najlepsze dopasowania, czyli zaczynam z n ścieżkami z reżyserem, potem znajduję m ścieżek np. z nazwą filmu. Dla każdej z n ścieżek dopasowuję do niej m ścieżek z nazwami, najlepsze dopasowanie zostaje zapisane w danej ścieżce z tablicy n-elementowej. Robię tak aż dochodzę do końca i wtedy ciągle mam n ścieżek. Sprawdzam, która z nich jest najdłuższa - oznacza to najlepsze dopasowanie(wcześniej odrzucam ścieżki niepożądane - zawierające znacznik meta, bo nagłówek mnie nie interesuje).

Jak użytkownik wybierze kilka stron do uczenia, to opisy jak powyżej są generowane dla każdej strony, a potem są łączone ze sobą. Może wtedy dojść pole "optional", które mówi, że jakiś atrybut nie występuje na każdej stronie. Podczas łączenia sprawdzam różne rzeczy:
- parametry long muszą się zgadzać
- multiple jest równe True, jeśli na którejkolwiek stronie jest równy True
- ścieżki są łączone: jak na stronie 1: [(div, 1), (p, 2)], a na 2: [(div, 2), (div, 1)], to dostaję [(div, "_"), ("_", "_")], "_" oznacza dowolną rzecz

Jak wykrywane są boldy? W trakcie uczenia sprawdzam, czy dany napis w całości występuje na stronie. Jeśli nie, to rozbijam go na wyrazy i szukam, gdzie występuje. Znajduję te wyrazy, potem znajduję ich ścieżki i biorę wspólną ścieżkę. Przeglądam je od najwyższego poziomu i wyjmuję tekst z poddrzewa:
A
-- B
----D
--E
to dostanę A B D E. Wtedy usuwam białe znaki pomiędzy wyrazami, wstawiam tam spacje i sprawdzam, czy pasuje to do początkowego napisu.

Teraz szukanie informacji na dowolnej (nie uczącej) stronie. Korzystam z opisu, który otrzymałem w wyniku łączenia napisów z kilku stron(może być z jednej). Na początku wyznaczam miejsce korzenia poddrzewa opisującego film: wybieram elementy zawierające klucz na stronie(keyVisible = True) i wyszukuję ich wspólną ścieżkę. W zależności od tego, jakie są to elementy, mogę dostać różny korzeń poddrzewa(bo to znalezione drzewa będzie obejmować tylko te elementy, a nie wszystkie). Dlatego sprawdzam, jaki jest wspólny przodek znalezionych elementów. Jeśli są elementy mające wspólnego przodka powyżej, to przesuwam się do góry o ilość różnych przodków. Teoretycznie powinno mi to umożliwić znalezienie właściwego przodka, ale jest problem, jeśli są pola ze ścieżką "_", bo wtedy nie wiem dokładnie, czy który element natrafiłem(przydałoby się dodać informację, które elementy mogą być na tym samym poziomie(być rodzeństwem, bo ułatwiłoby to tutaj wyszukiwanie wspólnego przodka), ale zabrakło czasu).
------------------------------------------
Poniższe nie jest zrobione:
Jak mam przodka, to mogę sprawdzić pola. Na początku pola obligatoryjne (optional=False) i mające widoczny na stronie klucz(np. napis Reżyseria). Znajduję klucz w poddrzewie i biorę jego ścieżkę. Sprawdzam, czy jest zgodna z opisem tego elementu. Potem mogę jeszcze sprawdzić zawartość pola, czy jest zgodne z opisem. Potem sprawdzam elementy bez klucza na stronie. Tutaj jest problem przy oznaczeniu, które stosuję ("_" jest zbyt ogólne), dlatego trudno jest sprawdzać, który może to być element. Można zmienić sposób opisu numeru pola, np. zamiast "_" listę numerów [2, 3] lub sprawdzać tylko zawartość i jak jest zgodna, to zakładać, że jest dobrze.
Pola nieobliagatoryjne sprawdzałbym podobnie, tylko z tą różnicą, że jak jakiegoś bym nie znalazł, to bym nie mówił, że błąd.

Wykrywanie boldów: podczas uczenia można by tworzyć parametr "split" dla elementów, które miały boldy. Wtedy byłyby sprawdzane pod kątem występowania boldów tylko elementy z takim parametrem. Lub można przejść przez drzewo i elementy zawierające znaczniki w środku tekstu.

To mniej więcej tak wygląda to, co chciałem zrobić. Jeszcze raz przepraszam,  że nie zrobiłem tego (nie to, że byłem leniwy, tylko może wybrałem złą metodę albo nie rozplanowałem tego tak, jak powinienem).

pozdro,
Bartek