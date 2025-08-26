import asyncio
import math
import moteus
import moteus_pi3hat
import time
import signal
import csv
import sys

shutdown = False

general_params = {
    "max_pow": 450,
    "max_cur": 80,
    "flux_min_v": 27.5,
    "flux_margin_v": 18.5,
}

def signal_handler(sig, frame):
    """Gestione del Ctrl+C per uno stop sicuro."""
    global shutdown
    print("\n\nRilevato Ctrl+C. Arresto sicuro...")
    shutdown = True

def log_results(data, results):
    """Scrive i risultati sul file CSV (una riga per ogni risultato)."""
    for result in results:
        data.write(
            f"{result.id},"
            f"{time.time():.6f},"
            f"{result.values.get(moteus.Register.POSITION, float('nan')):.6f},"
            f"{result.values.get(moteus.Register.VELOCITY, float('nan')):.6f},"
            f"{result.values.get(moteus.Register.TORQUE, float('nan')):.6f},"
            f"{result.values.get(moteus.Register.VOLTAGE, float('nan')):.3f},"
            f"{result.values.get(moteus.Register.TEMPERATURE, 0)},"
            f"{result.values.get(moteus.Register.FAULT, 0)}\n"
        )
    data.flush()

async def main():
    global shutdown
    signal.signal(signal.SIGINT, signal_handler)

    print("\n=== TEST IN COPPIA ===")
    print("1 = Test SINUSOIDALE NO LOAD (torque ±0.06 Nm, 1 minuto)")
    print("2 = Test TEMPERATURE (torque 0.5 Nm, 5 minuti)")
    choice = input("Seleziona il tipo di test [1/2]: ").strip()

    freq_tq = 0.25  # Hz
    offset_tq = 0.0

    if choice == "1":
        amp_tq = 0.06
        duration = 60.0
        label = "NO_LOAD"
        print(f"\nEsecuzione test {label}: ampiezza ±{amp_tq} Nm, durata {duration}s, freq {freq_tq} Hz")
    elif choice == "2":
        amp_tq = 0.5
        duration = 300.0
        torque_cmd = offset_tq + amp_tq
        label = "TEMPERATURE"
        print(f"\nEsecuzione test {label}: ampiezza {amp_tq} Nm, durata {duration}s")
    else:
        print("Scelta non valida. Uscita.")
        sys.exit(1)

    # --- Connessione al motore ---
    ch_act = 1
    id_act = 1
    transport = moteus_pi3hat.Pi3HatRouter(servo_bus_map={ch_act: [id_act]})
    servo = moteus.Controller(id=id_act, transport=transport)

    # --- Configurazione del motore ---
    s1 = moteus.Stream(servo)
    await s1.command(b'conf set servo.max_velocity 100')
    await s1.command(b'conf set servo.max_power_W 450')
    await s1.command(b'conf set servo.max_current_A 40')
    await s1.command(b'conf set servo.pid_position.kp 2')
    await s1.command(b'conf set servo.pid_position.kd 0.02')
    await s1.command(b'conf set servo.pid_position.ki 0.0')
    await s1.command(b'conf set servo.pid_position.ilimit 0')
    await s1.command(b'conf set servo.flux_brake_margin_voltage ' + str(general_params["flux_margin_v"]).encode('utf-8'))
    await s1.command(b'd exact 0.0')

    servopos = moteus.Controller(id=id_act, transport=transport)
    s2 = moteus.Stream(servopos)
    await s1.command(b'conf set servopos.position_min -3000')
    await s1.command(b'conf set servopos.position_max 3000')

    await transport.cycle([servo.make_stop()])
    print("\nConfigurazione completata.")

    # --- Apertura file log ---
    filename = f"log_attuatore_{label}.csv"
    with open(filename, "w", buffering=1) as data:
        data.write("id,timestamp,position,velocity,torque,voltage,temperature,fault\n")
        data.flush()

        print(f"\nInizio test {label}... (CTRL+C per interrompere)")
        start = time.time()
        next_update = 0
        try:
            while (time.time() - start) < duration and not shutdown:
                elapsed = time.time() - start

                # --- Controllo della coppia ---
                if choice == "1":
                    # # Impulso iniziale di coppia costante per partire
                    # if elapsed < 1.0:
                    #     torque_cmd = 0.1  # Nm costante per 1 secondo
                    # else:
                        torque_cmd = offset_tq + amp_tq * math.sin(2 * math.pi * freq_tq * elapsed)

                # --- Comando ---
                cmd = servo.make_position(
                    position=math.nan,
                    velocity=0.0,
                    feedforward_torque=torque_cmd,
                    kp_scale=0.0,
                    kd_scale=0.0,
                    ilimit_scale=0.0,
                    query=True
                )

                results = await transport.cycle([cmd])
                log_results(data, results)

                # Mostra il tempo ogni secondo
                if elapsed > next_update:
                    remaining = duration - elapsed
                    print(f"\rTempo trascorso: {elapsed:6.1f}s / {duration:.1f}s", end="")
                    next_update += 1

                await asyncio.sleep(0.01)

            print("\n\nTest completato.")

        finally:
            print("\nArresto motore...")
            await transport.cycle([servo.make_stop()])
            print(f"Uscita sicura. Log salvato in '{filename}'\n")

if __name__ == '__main__':
    asyncio.run(main())
