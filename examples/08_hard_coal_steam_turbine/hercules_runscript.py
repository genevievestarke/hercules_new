"""Example 07: Hard Coal Steam Turbine (HCST) simulation.

This example demonstrates a simple hard coal steam turbine (HCST) that:
- Starts on at rated capacity (100 MW)
- At 10 minutes, receives a shutdown command and begins ramping down
- At ~20 minutes, reaches 0 MW and transitions to off
- At 40 minutes, receives a turn-on command with a setpoint of 100% of rated capacity
- At ~80 minutes, 1 hour down-time minimum is reached and the turbine begins hot starting
- At ~87 minutes, hot start completes, continues ramping up to 100% of rated capacity
- At 120 minutes, receives a command to reduce power to 50% of rated capacity
- At 180 minutes, receives a command to reduce power to 10% of rated capacity
        (note this is below the minimum stable load)
- At 210 minutes, receives a command to increase power to 100% of rated capacity
- At 240 minutes (4 hours), receives a shutdown command
- Simulation runs for 6 hours total with 1 minute time steps
"""

from hercules.hercules_model import HerculesModel
from hercules.utilities_examples import prepare_output_directory

prepare_output_directory()

# Initialize the Hercules model
hmodel = HerculesModel("hercules_input.yaml")


class ControllerHCST:
    """Controller implementing the HCST schedule described in the module docstring."""

    def __init__(self, h_dict, component_name="hard_coal_steam_turbine"):
        """Initialize the controller.

        Args:
            h_dict (dict): The hercules input dictionary.

        """
        self.component_name = component_name
        self.rated_capacity = h_dict[self.component_name]["rated_capacity"]
        # Controller operates in 1-minute intervals, so base unit is an hour
        self.controller_base_unit = 45

    def step(self, h_dict):
        """Execute one control step.

        Args:
            h_dict (dict): The hercules input dictionary.

        Returns:
            dict: The updated hercules input dictionary.

        """
        current_time = h_dict["time"]

        # NOTE: update doc strings to reflect base unit scaling
        # Determine power setpoint based on time
        if current_time < 10 * self.controller_base_unit * 60:  # 10 minutes in seconds
            # Before 10 minutes: run at full capacity
            power_setpoint = self.rated_capacity
        elif current_time < 40 * self.controller_base_unit * 60:  # 40 minutes in seconds
            # Between 10 and 40 minutes: shut down
            power_setpoint = 0.0
        elif current_time < 120 * self.controller_base_unit * 60:  # 120 minutes in seconds
            # Between 40 and 120 minutes: signal to run at full capacity
            power_setpoint = self.rated_capacity
        elif current_time < 180 * self.controller_base_unit * 60:  # 180 minutes in seconds
            # Between 120 and 180 minutes: reduce power to 50% of rated capacity
            power_setpoint = 0.5 * self.rated_capacity
        elif current_time < 210 * self.controller_base_unit * 60:  # 210 minutes in seconds
            # Between 180 and 210 minutes: reduce power to 10% of rated capacity
            power_setpoint = 0.1 * self.rated_capacity
        elif current_time < 240 * self.controller_base_unit * 60:  # 240 minutes in seconds
            # Between 210 and 240 minutes: increase power to 100% of rated capacity
            power_setpoint = self.rated_capacity
        else:
            # After 240 minutes: shut down
            power_setpoint = 0.0

        h_dict[self.component_name]["power_setpoint"] = power_setpoint

        return h_dict


# Instantiate the controller and assign to the Hercules model
hmodel.assign_controller(ControllerHCST(hmodel.h_dict))

# Run the simulation
hmodel.run()

hmodel.logger.info("Process completed successfully")
