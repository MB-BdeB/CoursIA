import time
import random

output_path = r"C:\Users\Public\Documents\TELECHARGEMENT\BdeB\scripts\watchdog_output.txt"

def watchdog_logger(temps, temp_gpu, errors_ecc):
    log = f"[LOG - Sec {temps}] Température GPU: {temp_gpu}°C | Erreurs ECC: {errors_ecc}\n"
    print(log, end='')
    with open(output_path, 'a', encoding='utf-8') as f:
        f.write(log)

    if temp_gpu > 82:
        alert = "  --> [ALERT SYSTEM] Vitesse d'horloge bridée automatiquement (Thermal Throttling)!\n"
        print(alert, end='')
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write(alert)

    if errors_ecc > 10:
        crit = "  --> [CRITICAL ERROR] Trop d'erreurs ECC ! Isolation du nœud et basculement du calcul.\n"
        print(crit, end='')
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write(crit)
        return False

    return True

# Nettoyer le fichier de sortie
open(output_path, 'w', encoding='utf-8').close()

continuer_execution = True
for seconde in range(1, 11):
    if not continuer_execution:
        break
    temp_simulee = random.randint(70, 86)
    ecc_simulees = 0 if seconde < 6 else (seconde - 5) * 4
    continuer_execution = watchdog_logger(seconde, temp_simulee, ecc_simulees)
    time.sleep(1)

print(f"WROTE:{output_path}")
