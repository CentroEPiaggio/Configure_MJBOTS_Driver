import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def main():
    # Verifica che il file sia stato passato come argomento
    if len(sys.argv) < 2:
        print("Uso: python3 plot_csv_1.py <file_csv>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Controlla che il file esista
    if not os.path.exists(file_path):
        print(f"Errore: il file '{file_path}' non esiste.")
        sys.exit(1)

    print(f"Caricamento file: {file_path}")
    df = pd.read_csv(file_path)

    # Conversione timestamp e normalizzazione a t=0
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    time_sec = (df["timestamp"] - df["timestamp"].iloc[0]).dt.total_seconds()

    # Conversioni richieste
    df["position"] = df["position"] / 9.0
    df["velocity"] = df["velocity"] / 9.0
    df["torque"]   = df["torque"] * 9.0
    
    # Calcola medie mobili
    window_size = 100
    df["temp_smooth"] = df["temperature"].rolling(window=window_size, center=True).mean()
    df["position_smooth"] = df["position"].rolling(window=window_size, center=True).mean()
    df["velocity_smooth"] = df["velocity"].rolling(window=window_size, center=True).mean()

    # Calcola valori medi
    mean_pos = df["position"].mean()
    mean_vel = df["velocity"].mean()

    # Imposta layout con 3 subplot verticali
    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    fig.suptitle(f"Andamento grandezze attuatore nel tempo\n({os.path.basename(file_path)})")

    # === Posizione ===
    axes[0].plot(time_sec, df["position"], color="tab:blue", label="Position / 9")
    axes[0].plot(time_sec, df["position_smooth"], color="red", linestyle="--", label="Media mobile")
    axes[0].axhline(mean_pos, color="red", linestyle="--", label=f"Mean = {mean_pos:.4f}")
    axes[0].set_ylabel("Position / 9")
    axes[0].grid(True)
    axes[0].legend(loc="upper right")

    # === Velocità ===
    axes[1].plot(time_sec, df["velocity"], color="tab:orange", label="Velocity / 9")
    axes[1].plot(time_sec, df["velocity_smooth"], color="gray", linestyle="--", label="Media mobile")
    axes[1].axhline(mean_vel, color="red", linestyle="--", label=f"Mean = {mean_pos:.4f}")
    axes[1].set_ylabel("Velocity / 9")
    axes[1].grid(True)
    axes[1].legend(loc="upper right")

    # === Coppia e Temperatura ===
    ax_torque = axes[2]
    ax_temp = ax_torque.twinx()

    ax_torque.plot(time_sec, df["torque"], color="tab:green", label="Torque x9")
    ax_torque.set_ylabel("Torque x9", color="tab:green")
    ax_torque.tick_params(axis="y", labelcolor="tab:green")

    ax_temp.plot(time_sec, df["temperature"], color="tab:red", label="Temperature")
    ax_temp.plot(time_sec, df["temp_smooth"], color="blue", linestyle="--", label="Media temp")
    ax_temp.set_ylabel("Temp [°C]", color="tab:red")
    ax_temp.tick_params(axis="y", labelcolor="tab:red")

    ax_torque.grid(True)
    axes[3].plot(time_sec, df["voltage"], color="tab:orange", label="Voltage")
    axes[3].set_ylabel("Voltage")
    axes[3].grid(True)
    axes[3].legend(loc="upper right")

    axes[-1].set_xlabel("Tempo [s]")

    # Migliora il layout
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

if __name__ == "__main__":
    main()
