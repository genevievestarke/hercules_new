# Plot the outputs of the simulation for the OCGT example

import matplotlib.pyplot as plt
from hercules import HerculesOutput

# Read the Hercules output file using HerculesOutput
ho_ocgt = HerculesOutput("outputs/hercules_output_ocgt.h5")
ho_ccgt = HerculesOutput("outputs/hercules_output_ccgt.h5")

# Print metadata information
print("Simulation Metadata:")
ho_ocgt.print_metadata()
print()

# Create a shortcut to the dataframe
df_ocgt = ho_ocgt.df
df_ccgt = ho_ccgt.df

# Get the h_dict from metadata
h_dict_ocgt = ho_ocgt.h_dict
h_dict_ccgt = ho_ccgt.h_dict

# Convert time to minutes for easier reading
time_hours_ocgt = df_ocgt["time"] / 60 / 60
time_hours_ccgt = df_ccgt["time"] / 60 / 60

fig, axarr = plt.subplots(4, 1, sharex=True, figsize=(10, 10))

# Plot the power output and setpoint
ax = axarr[0]
ax.axhline(
    h_dict_ocgt["open_cycle_gas_turbine"]["rated_capacity"] / 1000,
    color="gray",
    linestyle=":",
    label="Rated Capacity",
)
ax.plot(
    time_hours_ocgt,
    df_ocgt["open_cycle_gas_turbine.power"] / 1000,
    label="OCGT Power Output",
    color="darkred",
)
ax.plot(
    time_hours_ocgt,
    df_ocgt["open_cycle_gas_turbine.power_setpoint"] / 1000,
    label="OCGT Power Setpoint",
    color="r",
    linestyle="--",
)
ax.axhline(
    h_dict_ocgt["open_cycle_gas_turbine"]["min_stable_load_fraction"]
    * h_dict_ocgt["open_cycle_gas_turbine"]["rated_capacity"]
    / 1000,
    color="rosybrown",
    linestyle="--",
    label="OCGT Minimum Stable Load",
)
ax.plot(
    time_hours_ccgt,
    df_ccgt["combined_cycle_gas_turbine.power"] / 1000,
    label="CCGT Power Output",
    color="darkblue",
)
ax.plot(
    time_hours_ccgt,
    df_ccgt["combined_cycle_gas_turbine.power_setpoint"] / 1000,
    label="CCGT Power Setpoint",
    color="dodgerblue",
    linestyle="--",
)
# ax.axhline(
#     h_dict_ccgt["combined_cycle_gas_turbine"]["rated_capacity"] / 1000,
#     color="gray",
#     linestyle=":",
#     label="Rated Capacity",
# )
ax.axhline(
    h_dict_ccgt["combined_cycle_gas_turbine"]["min_stable_load_fraction"]
    * h_dict_ccgt["combined_cycle_gas_turbine"]["rated_capacity"]
    / 1000,
    color="lightsteelblue",
    linestyle="--",
    label="CCGT Minimum Stable Load",
)
ax.set_ylabel("Power [MW]")
ax.set_title("Gas Turbine Power Output")
ax.legend()
ax.grid(True)

# Plot the state
ax = axarr[1]
ax.plot(time_hours_ocgt, df_ocgt["open_cycle_gas_turbine.state"], label="OCGT State", color="k")
ax.plot(
    time_hours_ccgt,
    df_ccgt["combined_cycle_gas_turbine.state"],
    label="CCGT State",
    color="gray",
    linestyle="--",
)
ax.set_ylabel("State")
ax.set_yticks([0, 1, 2, 3, 4, 5])
ax.set_yticklabels(["Off", "Hot Starting", "Warm Starting", "Cold Starting", "On", "Stopping"])
ax.set_title(
    "Turbine State (0=Off, 1=Hot Starting, 2=Warm Starting, 3=Cold Starting, 4=On, 5=Stopping)"
)
ax.legend()
ax.grid(True)

# Plot the efficiency
ax = axarr[2]
ax.plot(
    time_hours_ocgt,
    df_ocgt["open_cycle_gas_turbine.efficiency"] * 100,
    label="OCGT Efficiency",
    color="g",
)
ax.plot(
    time_hours_ccgt,
    df_ccgt["combined_cycle_gas_turbine.efficiency"] * 100,
    label="CCGT Efficiency",
    color="darkgreen",
    linestyle="--",
)
ax.legend()
ax.set_ylim(0, 100)
ax.set_ylabel("Efficiency [%]")
ax.set_title("Thermal Efficiency")
ax.grid(True)

# Plot the fuel consumption
ax = axarr[3]
ax.plot(
    time_hours_ocgt,
    df_ocgt["open_cycle_gas_turbine.fuel_volume_rate"],
    label="OCGT Fuel Volume Rate",
    color="orange",
)
ax.plot(
    time_hours_ccgt,
    df_ccgt["combined_cycle_gas_turbine.fuel_volume_rate"],
    label="CCGT Fuel Volume Rate",
    color="darkorange",
    linestyle="--",
)
ax.legend()
ax.set_ylabel("Fuel [m³/s]")
ax.set_title("Fuel Volume Rate")
ax.grid(True)

ax.set_xlabel("Time [hours]")

plt.tight_layout()
plt.show()
