# LASER Fast-LIO Core

This package serves as the **core integration point** for the Fast-LIO (Fast LiDAR-Inertial Odometry) algorithm within the Laser UAV System (LUS). It acts as a configuration manager and launch wrapper, ensuring that the standard `fast_lio` node runs correctly with the specific parameters, topic remappings, and namespace configurations required by the drone architecture.

## Overview

The `laser_fast_lio_core` package is responsible for:
1.  **Orchestration:** Launching the Fast-LIO mapping node with dynamic ROS 2 namespaces.
2.  **Configuration Management:** storing specific parameter files for different LiDAR/IMU setups (e.g., Livox Mid360 with internal or external IMU).
3.  **Topic Abstraction:** Handling the remapping of input PointCloud and IMU topics to match the LUS standard.

## Dependencies

This package depends on:
-   **`fast_lio`**: The core LIO algorithm package.
-   **`ros_environment`**: For environment variable handling (optional but recommended).

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

The `params/` directory contains configuration files for specific sensor setups. These files control the behavior of the Fast-LIO filter, including extrinsics and covariance tuning.

### Example Config (`mid360_external.yaml`)
Key parameters include:

```yaml
# Sensor Preprocessing
preprocess:
  lidar_type: 1       # 1 for Livox serials LiDAR (e.g., Mid360)
  scan_line: 16
  scan_rate: 10
  timestamp_unit: 3

# Mapping & Extrinsics
mapping:
  extrinsic_est_en: true  # Online estimation of IMU-LiDAR extrinsics
  extrinsic_T: [-0.0, -0.0, 0.0]
  extrinsic_R: [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

# Publishing Settings
publish:
  path_en: true           # Publish the trajectory path
  scan_publish_en: true   # Publish the registered scan
  scan_bodyframe_pub_en: true # Output scans in the IMU-body-frame
  dense_publish_en: true  # Dense point cloud output

# Frame Definitions
transform:
  fcu_frame: "uav1/fcu"
  world_frame: "uav1/world"
  lidar_frame: "uav1/livox_lidar"
  imu_frame: "uav1/livox_imu"