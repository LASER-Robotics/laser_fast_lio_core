# LASER Fast-LIO Core

This package serves as the **core integration point** for the Fast-LIO (Fast LiDAR-Inertial Odometry) algorithm within the Laser UAV System (LUS). It acts as a configuration manager and launch wrapper, ensuring that the standard `fast_lio` node runs correctly with the specific parameters, topic remappings, and namespace configurations required by the drone architecture.

## Overview

The `laser_fast_lio_core` package is responsible for:
1.  **Orchestration:** Launching the Fast-LIO mapping node with dynamic ROS 2 namespaces.
2.  **Configuration Management:** storing specific parameter files for different LiDAR/IMU setups (e.g., Livox Mid360 with internal or external IMU).
3.  **Topic Abstraction:** Handling the remapping of input PointCloud and IMU topics to match the LUS standard.

## How It Works

This package creates an abstraction layer over the standard FAST_LIO launch process. Instead of hardcoding paths or editing core configuration files for different setups, the launch files here accept arguments to select the hardware profile and topics dynamically.

### 1. Dynamic Parameter Loading
The system uses the `fast_lio_config_file_path` argument to locate the specific configuration file for the algorithm.
-   Inside the `params/` directory, you can define different YAML files for various sensor setups (e.g., `mid360_internal.yaml` for internal IMU usage or `mid360_external.yaml` for external IMU integration).
-   When the launch file runs, it passes this specific path to the underlying FAST_LIO mapping node.
-   This allows you to switch between different LiDAR models or mounting configurations (extrinsics) without modifying the source code.

### 2. Topic and Namespace Abstraction
The launch file accepts generic arguments for sensor topics (`topic_imu`, `topic_pcl`) and handles the remapping to the estimator's expected inputs.
-   It relies on the `namespace` argument (defaulting to the `UAV_NAME` environment variable) to ensure multi-robot compatibility.
-   This ensures that the FAST_LIO node publishes odometry and map data under the correct robot namespace (e.g., `/uav1/fast_lio/...`).

### 3. Visualization Helpers
To make debugging easier in multi-agent simulations, this package includes scripts (specifically `scripts/refactor_rviz_config.sh`) that automatically update RViz configuration files.
-   Before launching RViz, the script creates a temporary copy of the default config and replaces generic placeholders (like `uav1`) with the current `UAV_NAME`.
-   This prevents the common issue of RViz listening to `/uav1/fast_lio/cloud_registered` when you are actually flying `uav2`.

## Launch Files

### 1. `fast_lio.launch.py`
This is the main launch file to start the LiDAR-Inertial Odometry estimator. It wraps the standard `mapping.launch.py` from the `fast_lio` package but exposes arguments for easy integration.

-   **Usage:**
    ```bash
    ros2 launch laser_fast_lio_core fast_lio.launch.py \
        topic_imu:=/uav1/livox/imu \
        topic_pcl:=/uav1/livox/lidar \
        fast_lio_config_file_path:=$(ros2 pkg prefix --share laser_fast_lio_core)/params/mid360_external.yaml
    ```

-   **Arguments:**
    -   `namespace` (default: `uav1`): Top-level namespace for the drone.
    -   `use_sim_time` (default: `false`): Set to `true` if running in simulation.
    -   `topic_pcl` (default: empty): The input PointCloud2 topic name.
    -   `topic_imu` (default: empty): The input IMU topic name.
    -   `fast_lio_config_file_path`: Full path to the YAML configuration file. Defaults to `params/mid360_internal.yaml`.

## Configuration

The `params/` directory contains configuration files for specific sensor settings. These files control the behavior of the Fast-LIO filter, including extrinsic parameters, covariance adjustment, and point cloud preprocessing.

- `mid360_external.yaml`: Configuration for performing external flights. Defines the extrinsic parameters between the LiDAR and the internal inertial unit.

- `mid360_internal.yaml`: Configuration for performing internal flights. Defines the extrinsic parameters between the LiDAR and the internal inertial unit.

### Helper Scripts

The package includes scripts in the `scripts/` directory to facilitate visualization:
-   `refactor_rviz_config.sh`: Automatically updates RViz configuration files with the correct UAV namespace.
-   `refactor_plotjuggler_config.sh`: Automatically updates PlotJuggler layouts.
