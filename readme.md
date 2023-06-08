


# Sterownik Raspberry pi PICO z obsługą czujników temperatury DS18B20

Ten projekt Arduino służy do sterowania czterema wyjściami GPIO (H1, H2, H3, P1) oraz do odczytywania temperatury z dwóch czujników DS18B20 (T1, T2).

## Schemat pinów
Piny GPIO zdefiniowane w projekcie to:
- H1 -> Pin 18
- H2 -> Pin 19
- H3 -> Pin 20
- P1 -> Pin 21
- DS18B20 -> Pin 6 (Dla obu czujników)

## Sterowanie
Sterowanie odbywa się przez port szeregowy. Możesz wysłać następujące komendy do sterowania pinami GPIO:
- H1-ON
- H1-OFF
- H2-ON
- H2-OFF
- H3-ON
- H3-OFF
- P1-ON
- P1-OFF

Po poprawnym wykonaniu każdej komendy sterującej, Arduino odeśle potwierdzenie w postaci odebranej komendy z dopiskiem "-OK". Na przykład, po otrzymaniu komendy "H1-ON", Arduino odesłać "H1-ON-OK".

## Odczyt temperatury
Aby odczytać temperaturę z czujników DS18B20, można wysłać następujące komendy:
- T0-?
- T1-?
- T2-?
- T3-?


Arduino odpowie poprzez przesłanie temperatury w formie "T1-XX.XC" lub "T2-XX.XC", gdzie XX.X to odczytana temperatura. Na koniec otrzymasz potwierdzenie w postaci "T1-?-OK" lub "T2-?-OK".

## Biblioteki
Ten projekt korzysta z następujących bibliotek Arduino:
- OneWire
- DallasTemperature

