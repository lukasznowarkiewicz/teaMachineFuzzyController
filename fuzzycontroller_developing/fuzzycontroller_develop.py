import numpy as np
import skfuzzy as fuzz
import skfuzzy.membership as mb
import matplotlib.pyplot as plt

# Inicjalizacja
temp_max = 100.0
heater_power = 10
desired_temperature = 80.0 # Stała do zdefiniowania temperatury zadanej
inlet_temperature = 23 
desired_t0=(desired_temperature-inlet_temperature)/3*1
desired_t1=(desired_temperature-inlet_temperature)/3*2
desired_t2=(desired_temperature-inlet_temperature)/3*3
desired_t3=desired_temperature
print("Desired T0: " + str(round(desired_t0)) + " Desired T1: " + str(round(desired_t1)) + " Desired T2: " + str(round(desired_t2)) + " Desired T3: " + str(round(desired_t3)))

read_t0=16 # zmienne na przyszłość do przypisywania wartości odczytywanych z czujników temperatury
read_t1=read_t0*1.8
read_t2=read_t0*2.6
read_t3=read_t0*4

# Zmienne
x_t0 = np.arange(0, temp_max, 1)
x_t1 = np.arange(0, temp_max, 1)
x_t2 = np.arange(0, temp_max, 1)
x_t3 = np.arange(0, temp_max, 1)
print("Read T0: " + str(round(read_t0)) + " READ T1: " + str(round(read_t1)) + " READ T2: " + str(round(read_t2)) + " READ T3: " + str(round(read_t3)))
y_t_desired = np.arange(0, temp_max, 1)


# Funkcje członkowstwa - powinny być tablicami floatów
t0_cold = mb.trapmf(x_t0, [-20, -10, desired_t0-10, desired_t0-5])
t0_ok = mb.trapmf(x_t0, [desired_t0-10, desired_t0-5, desired_t0+5, desired_t0+10])
t0_hot = mb.trapmf(x_t0, [desired_t0+5, desired_t0+10, 110, 120])

t1_cold = mb.trapmf(x_t1, [-20, -10, desired_t1-10, desired_t1-5])
t1_ok = mb.trapmf(x_t1, [desired_t1-10, desired_t1-5, desired_t1+5, desired_t1+10])
t1_hot = mb.trapmf(x_t1, [desired_t1+5, desired_t1+10, 110, 120])

t2_cold = mb.trapmf(x_t2, [-20, -10, desired_t2-10, desired_t2-5])
t2_ok = mb.trapmf(x_t2, [desired_t2-10, desired_t2-5, desired_t2+5, desired_t2+10])
t2_hot = mb.trapmf(x_t2, [desired_t2+5, desired_t2+10, 110, 120])

t3_cold = mb.trapmf(x_t3, [-20, -10, desired_t3-10, desired_t3-5])
t3_ok = mb.trapmf(x_t3, [desired_t3-10, desired_t3-5, desired_t3+5, desired_t3+10])
t3_hot = mb.trapmf(x_t3, [desired_t3+5, desired_t3+10, 110, 120])

# Funkcje członkowstwa dla wyjścia - równie tablice floatów

# wersja ze skalowaniem zakresow jak są powyzej 70 stopni zeby nie przekroczyc 100 stopni
temp_step = 2 * desired_temperature / 7.5

temp_very_very_low = mb.trapmf(y_t_desired, [0, 0, temp_step, 1.5*temp_step])
temp_very_low = mb.trapmf(y_t_desired, [temp_step, 1.5*temp_step, 2*temp_step, 2.5*temp_step])
temp_low = mb.trapmf(y_t_desired, [2*temp_step, 2.5*temp_step, 3*temp_step, 3.5*temp_step])
temp_ok = mb.trapmf(y_t_desired, [3*temp_step, 3.5*temp_step, 4*temp_step, 4.5*temp_step])

if desired_temperature > 60:
    temp_high_pivot = (temp_max-desired_temperature)/4
    temp_very_high_pivot=2*(temp_max-desired_temperature)/4
    temp_very_very_high_pivot=3*(temp_max-desired_temperature)/4
    temp_high = mb.trapmf(y_t_desired, [desired_temperature+temp_high_pivot-temp_high_pivot*0.5, desired_temperature+temp_high_pivot-temp_high_pivot*0.25, desired_temperature+temp_high_pivot+temp_high_pivot*0.25, desired_temperature+temp_high_pivot+temp_high_pivot*0.5])
    temp_very_high = mb.trapmf(y_t_desired, [desired_temperature+temp_very_high_pivot-temp_very_high_pivot*0.5, desired_temperature+temp_very_high_pivot-temp_very_high_pivot*0.25, desired_temperature+temp_very_high_pivot+temp_very_high_pivot*0.25, desired_temperature+temp_very_high_pivot+temp_very_high_pivot*0.5])
    temp_very_very_high = mb.trapmf(y_t_desired, [desired_temperature+temp_very_very_high_pivot-temp_very_very_high_pivot*0.5, desired_temperature+temp_very_very_high_pivot-temp_very_very_high_pivot*0.25, desired_temperature+temp_very_very_high_pivot+temp_very_high_pivot*0.25, desired_temperature+temp_very_very_high_pivot+temp_very_very_high_pivot*0.5])
else:
    scaling_factor = 1
    temp_high = mb.trapmf(y_t_desired, [scaling_factor * 4*temp_step, scaling_factor * 4.5*temp_step, scaling_factor * 5*temp_step, scaling_factor * 5.5*temp_step])
    temp_very_high = mb.trapmf(y_t_desired, [scaling_factor * 5*temp_step, scaling_factor * 5.5*temp_step, scaling_factor * 6*temp_step, scaling_factor * 6.5*temp_step])
    temp_very_very_high = mb.trapmf(y_t_desired, [scaling_factor * 5.5*temp_step, scaling_factor * 6*temp_step, 2*min(desired_temperature, 100)-1, 2*min(desired_temperature, 100)])





# Odrozmywanie

# Wykres
# fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows = 4, figsize =(10, 10))

# ax0.plot(x_t0, t0_cold, 'r', linewidth = 2, label = 'za zimno')
# ax0.plot(x_t0, t0_ok, 'g', linewidth = 2, label = 'ok')
# ax0.plot(x_t0, t0_hot, 'b', linewidth = 2, label = 'za cieplo')
# ax0.set_title('Temperatura T0')
# ax0.legend()

# ax1.plot(x_t1, t1_cold, 'r', linewidth = 2, label = 'za zimno')
# ax1.plot(x_t1, t1_ok, 'g', linewidth = 2, label = 'ok')
# ax1.plot(x_t1, t1_hot, 'b', linewidth = 2, label = 'za cieplo')
# ax1.set_title('Temperatura T1')
# ax1.legend()

# ax2.plot(x_t2, t2_cold, 'r', linewidth = 2, label = 'za zimno')
# ax2.plot(x_t2, t2_ok, 'g', linewidth = 2, label = 'ok')
# ax2.plot(x_t2, t2_hot, 'b', linewidth = 2, label = 'za cieplo')
# ax2.set_title('Temperatura T2')
# ax2.legend()

# ax3.plot(x_t3, t3_cold, 'r', linewidth = 2, label = 'za zimno')
# ax3.plot(x_t3, t3_ok, 'g', linewidth = 2, label = 'ok')
# ax3.plot(x_t3, t3_hot, 'b', linewidth = 2, label = 'za cieplo')
# ax3.set_title('Temperatura T3')
# ax3.legend()

# plt.tight_layout()
# plt.show()


# Stopień członkowstwa - rozmywanie - wyrzuca pojedyncze floaty
t0_fit_cold = fuzz.interp_membership(x_t0, t0_cold, read_t0)
t0_fit_ok = fuzz.interp_membership(x_t0, t0_ok, read_t0)
t0_fit_hot = fuzz.interp_membership(x_t0, t0_hot, read_t0)

t1_fit_cold = fuzz.interp_membership(x_t1, t1_cold, read_t1)
t1_fit_ok = fuzz.interp_membership(x_t1, t1_ok, read_t1)
t1_fit_hot = fuzz.interp_membership(x_t1, t1_hot, read_t1)

t2_fit_cold = fuzz.interp_membership(x_t2, t2_cold, read_t2)
t2_fit_ok = fuzz.interp_membership(x_t2, t2_ok, read_t2)
t2_fit_hot = fuzz.interp_membership(x_t2, t2_hot, read_t2)

t3_fit_cold = fuzz.interp_membership(x_t3, t3_cold, read_t3)
t3_fit_ok = fuzz.interp_membership(x_t3, t3_ok, read_t3)
t3_fit_hot = fuzz.interp_membership(x_t3, t3_hot, read_t3)


print(f"T0 fits: Cold: {t0_fit_cold}, OK: {t0_fit_ok}, Hot: {t0_fit_hot}")
print(f"T1 fits: Cold: {t1_fit_cold}, OK: {t1_fit_ok}, Hot: {t1_fit_hot}")
print(f"T2 fits: Cold: {t2_fit_cold}, OK: {t2_fit_ok}, Hot: {t2_fit_hot}")
print(f"T3 fits: Cold: {t3_fit_cold}, OK: {t3_fit_ok}, Hot: {t3_fit_hot}")


# Zasady - powinny byc jako array floatów
# # 3 za zimno
rule1 = np.fmin(np.fmin(np.fmin(np.fmin(t0_fit_cold, t1_fit_cold), t2_fit_cold), t3_fit_cold),temp_very_very_low)

# 2 za zimno
rule2 = np.fmin(np.fmin(np.fmin(t0_fit_cold, t1_fit_cold), np.fmin(t2_fit_ok, t3_fit_ok)),temp_very_low)
rule3 = np.fmin(np.fmin(np.fmin(t0_fit_cold, t2_fit_cold), np.fmin(t1_fit_ok, t3_fit_ok)),temp_very_low)
rule4 = np.fmin(np.fmin(np.fmin(t0_fit_cold, t3_fit_cold), np.fmin(t1_fit_ok, t2_fit_ok)),temp_very_low)
rule5 = np.fmin(np.fmin(np.fmin(t1_fit_cold, t2_fit_cold), np.fmin(t0_fit_ok, t3_fit_ok)),temp_very_low)
rule6 = np.fmin(np.fmin(np.fmin(t1_fit_cold, t3_fit_cold), np.fmin(t0_fit_ok, t2_fit_ok)),temp_very_low)
rule7 = np.fmin(np.fmin(np.fmin(t2_fit_cold, t3_fit_cold), np.fmin(t0_fit_ok, t1_fit_ok)),temp_very_low)

# 1 za zimno
rule8 = np.fmin(np.fmin(t0_cold, np.fmin(np.fmin(t1_fit_ok, t2_fit_ok), t3_fit_ok)),temp_low)
rule9 = np.fmin(np.fmin(t1_fit_cold, np.fmin(np.fmin(t0_fit_ok, t2_fit_ok), t3_fit_ok)),temp_low)
rule10 = np.fmin(np.fmin(t2_fit_cold, np.fmin(np.fmin(t0_fit_ok, t1_fit_ok), t3_fit_ok)),temp_low)
rule11 = np.fmin(np.fmin(t3_fit_cold, np.fmin(np.fmin(t0_fit_ok, t1_fit_ok), t2_fit_ok)),temp_low)

# wszystkie ok
rule12 = np.fmin(np.fmin(np.fmin(np.fmin(t0_fit_ok, t1_fit_ok), t2_fit_ok), t3_fit_ok),temp_ok)

# 1 za ciepło
rule13 = np.fmin(np.fmin(t0_fit_hot, np.fmin(np.fmin(t1_fit_ok, t2_fit_ok), t3_fit_ok)),temp_high)
rule14 = np.fmin(np.fmin(t1_fit_hot, np.fmin(np.fmin(t0_fit_ok, t2_fit_ok), t3_fit_ok)),temp_high)
rule15 = np.fmin(np.fmin(t2_fit_hot, np.fmin(np.fmin(t0_fit_ok, t1_fit_ok), t3_fit_ok)),temp_high)
rule16 = np.fmin(np.fmin(t3_fit_hot, np.fmin(np.fmin(t0_fit_ok, t1_fit_ok), t2_fit_ok)),temp_high)

# 2 za ciepło
rule17 = np.fmin(np.fmin(np.fmin(t0_fit_hot, t1_fit_hot), np.fmin(t2_fit_ok, t3_fit_ok)),temp_very_high)
rule18 = np.fmin(np.fmin(np.fmin(t0_fit_hot, t2_fit_hot), np.fmin(t1_fit_ok, t3_fit_ok)),temp_very_high)
rule19 = np.fmin(np.fmin(np.fmin(t0_fit_hot, t3_fit_hot), np.fmin(t1_fit_ok, t2_fit_ok)),temp_very_high)
rule20 = np.fmin(np.fmin(np.fmin(t1_fit_hot, t2_fit_hot), np.fmin(t0_fit_ok, t3_fit_ok)),temp_very_high)
rule21 = np.fmin(np.fmin(np.fmin(t1_fit_hot, t3_fit_hot), np.fmin(t0_fit_ok, t2_fit_ok)),temp_very_high)
rule22 = np.fmin(np.fmin(np.fmin(t2_fit_hot, t3_fit_hot), np.fmin(t0_fit_ok, t1_fit_ok)),temp_very_high)

# 3 za ciepło
rule23 = np.fmin(np.fmin(np.fmin(np.fmin(t0_fit_hot, t1_fit_hot), t2_fit_hot), t3_fit_hot),temp_very_very_high)

rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, 
          rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, 
          rule22, rule23]

# for i, rule in enumerate(rules, start=1):
#       print(f"Rule {i}: {rule}")


# Zestawy zaagregowane
out_very_very_cold = rule1
out_very_cold = np.fmax(rule2, np.fmax(rule3, np.fmax(rule4, np.fmax(rule5, np.fmax(rule6, rule7)))))
out_cold = np.fmax(rule8, np.fmax(rule9, np.fmax(rule10, rule11)))
out_ok = rule12
out_hot = np.fmax(rule13, np.fmax(rule14, np.fmax(rule15, rule16)))
out_very_hot = np.fmax(rule17, np.fmax(rule18, np.fmax(rule19, np.fmax(rule20, np.fmax(rule21, rule22)))))
out_very_very_hot = rule23


# outputs = [out_very_very_cold, out_very_cold, out_cold, out_ok, out_hot, out_very_hot, out_very_very_hot]
# output_names = ["Very very cold", "Very cold", "Cold", "OK", "Hot", "Very hot", "Very very hot"]

# for name, output in zip(output_names, outputs):
#      print(f"{name}: {output}")


#wysterowac grzalki wedlug cold,ok,hot

# if(t1_fit_cold+t1_fit_ok > t1_fit_hot):
#     #send H1-ON
# else:
#     #send H1-OFF



# Odrozmywanie
# out_temp = np.fmax(out_very_very_cold, np.fmax(out_very_cold, np.fmax(out_cold, np.fmax(out_ok, np.fmax(out_hot, np.fmax(out_very_hot, np.fmax(out_very_hot, out_very_very_hot)))))))
# print(f"out temp: {out_temp}")
# defuzzified = fuzz.defuzz(y_t_desired, out_temp, 'centroid')
# result = fuzz.interp_membership(y_t_desired, out_temp, defuzzified)
# print("Status grzania:", defuzzified)
# print("Result:", result)

# niech wyprintuje jaka jest temperatura wedlug sterownika rozmytego

# Wykres

# risk0 = np.zeros_like(y_t_desired)
# fig, ax0 = plt.subplots(figsize = (7, 4))
# ax0.plot(y_t_desired, temp_very_very_low, 'r', linestyle = '--')
# ax0.plot(y_t_desired, temp_very_low, 'g', linestyle = '--')
# ax0.plot(y_t_desired, temp_low, 'b', linestyle = '--')
# ax0.plot(y_t_desired, temp_ok, 'y', linestyle = '--')
# ax0.plot(y_t_desired, temp_high, 'm', linestyle = '--')
# ax0.plot(y_t_desired, temp_very_high, 'c', linestyle = '--')
# ax0.plot(y_t_desired, temp_very_very_high, 'purple', linestyle = '--')
# ax0.fill_between(y_t_desired, risk0, out_temp, facecolor = 'Orange', alpha = 0.7)
# ax0.plot([defuzzified , defuzzified], [0, result], 'k', linewidth = 1.5, alpha = 0.9)
# ax0.set_title('Centroid Defuzzification')
# plt.tight_layout()
# plt.show()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


if max(t1_fit_cold, t1_fit_ok, t1_fit_hot) == t1_fit_cold:
    H1ctrlcmd = 'H1-ON'
elif max(t1_fit_cold, t1_fit_ok, t1_fit_hot) == t1_fit_ok:
    H1ctrlcmd = 'H1-OFF'
else:
    H1ctrlcmd = 'H1-OFF'
print(H1ctrlcmd)


if max(t2_fit_cold, t2_fit_ok, t2_fit_hot) == t2_fit_cold:
    H2ctrlcmd = 'H2-ON'
elif max(t2_fit_cold, t2_fit_ok, t2_fit_hot) == t2_fit_ok:
    H2ctrlcmd = 'H2-OFF'
else:
    H2ctrlcmd = 'H2-OFF'
print(H2ctrlcmd)


if max(t3_fit_cold, t3_fit_ok, t3_fit_hot) == t3_fit_cold:
    H3ctrlcmd = 'H3-ON'
elif max(t3_fit_cold, t3_fit_ok, t3_fit_hot) == t3_fit_ok:
    H3ctrlcmd = 'H3-OFF'
else:
    H3ctrlcmd = 'H3-OFF'
print(H3ctrlcmd)
