# LASER FAST-LIO Core

`laser_fast_lio_core` integrates FAST-LIO into the LASER UAV System (LUS). It supplies sensor profiles, launch files and visualization settings; the `fast_lio` dependency runs the LiDAR-inertial estimator.

FAST-LIO odometry feeds the estimation manager. Its registered point clouds can also feed ROG-Map and the obstacle-aware planner.

## Install and run

This repository contains the integration package under `ros_packages/laser_fast_lio_core` and fetches FAST-LIO through [.gitman.yml](.gitman.yml). Install the dependencies from this directory:

```bash
gitman install
```

With the component ROS packages available in your workspace:

```bash
colcon build --packages-up-to laser_fast_lio_core
source install/setup.bash
export UAV_NAME=uav1
ros2 launch laser_fast_lio_core fast_lio.launch.py topic_imu:=/uav1/livox/imu topic_pcl:=/uav1/livox/lidar
```

The wrapper starts FAST-LIO's `mapping.launch.py`. Start the LiDAR and IMU data sources separately.

## Interfaces

With `UAV_NAME=uav1` and the supplied mapping launch:

| Direction | Topic | Type | Purpose |
| --- | --- | --- | --- |
| Input | Selected by `topic_pcl` | `sensor_msgs/msg/PointCloud2` | LiDAR scans with fields matching the selected preprocessing mode. |
| Input | Selected by `topic_imu` | `sensor_msgs/msg/Imu` | Inertial measurements. |
| Output | `/uav1/fast_lio/odometry` | `nav_msgs/msg/Odometry` | Scan-corrected odometry. |
| Output | `/uav1/fast_lio/odometry_high_freq` | `nav_msgs/msg/Odometry` | High-frequency state used by the estimation manager. |
| Output | `/uav1/fast_lio/cloud_registered` | `sensor_msgs/msg/PointCloud2` | Registered cloud for mapping. |
| Output | `/uav1/fast_lio/cloud_registered_body` | `sensor_msgs/msg/PointCloud2` | Cloud in the body frame. |
| Output | `/uav1/fast_lio/cloud_effected`, `/uav1/fast_lio/laser_map` | `sensor_msgs/msg/PointCloud2` | Selected points and map visualization. |
| Output | `/uav1/fast_lio/imu/out` | `sensor_msgs/msg/Imu` | IMU output from the estimator. |
| Output | `/uav1/fast_lio/path` | `nav_msgs/msg/Path` | Estimated path. |
| Service | `/uav1/map_save` | `std_srvs/srv/Trigger` | Saves the map when PCD recording is enabled. |

Cloud and path publication depend on the profile settings. Frame names come from the configuration and TF, so topic namespace and coordinate frame must be checked together.

## Configuration

### Launch arguments

| Argument | Default | Meaning |
| --- | --- | --- |
| `namespace` | `UAV_NAME`, or `uav1` | Declared by the wrapper. The current wrapper does not forward it to FAST-LIO; set `UAV_NAME` for the underlying launch. |
| `use_sim_time` | `true` when `REAL_UAV=false` | Uses the simulation clock. |
| `topic_pcl`, `topic_imu` | Empty in the wrapper | LiDAR and IMU inputs; pass both explicitly. |
| `fast_lio_config_file_path` | Installed `params/mid360_internal.yaml` | Full path to the sensor configuration. |

### Sensor profiles

The profiles are in [ros_packages/laser_fast_lio_core/params/](ros_packages/laser_fast_lio_core/params/). `mid360_internal.yaml` and `mid360_external.yaml` currently have the same tuning and extrinsics; the names alone do not select different IMU hardware. `fast_lio_outside.yaml` is another supplied profile.

| Parameter group | Meaning |
| --- | --- |
| `point_filter_num`, `filter_size_surf`, `filter_size_map` | Point thinning and surface/map voxel sizes. |
| `max_iteration`, `cube_side_length` | Estimator iteration limit and local map dimensions. |
| `common.time_sync_en`, `common.time_offset_lidar_to_imu` | Software synchronization and LiDAR-to-IMU time offset. Prefer synchronized sensor timestamps. |
| `preprocess.lidar_type`, `scan_line`, `timestamp_unit`, `scan_rate`, `blind` | Point format, scan structure, per-point time units, scan rate and minimum retained range. |
| `mapping.acc_cov`, `gyr_cov`, `b_acc_cov`, `b_gyr_cov` | Accelerometer, gyroscope and bias noise settings. |
| `mapping.extrinsic_T`, `mapping.extrinsic_R` | LiDAR pose in the IMU frame: translation and a row-major 3×3 rotation matrix. |
| `mapping.extrinsic_est_en` | Enables online extrinsic estimation. |
| `mapping.fov_degree`, `mapping.det_range` | Mapping field of view and detection range. |
| `publish.*` | Enables path, registered clouds, body-frame clouds and map output. |
| `pcd_save.pcd_save_en`, `pcd_save.interval`, `map_file_path` | Enables PCD recording and selects save interval and output path. An interval of `-1` accumulates all scans, which can consume substantial memory. |
| `imu_in_gravity_unit` | `true` for acceleration in g; `false` for m/s². |
| `velocity_in_body_frame` | Selects body-frame rather than world-frame velocity output. |
| `transform.*` | TF enable flags and FCU, world, LiDAR and IMU frame names. |
| `runtime_pos_log_enable` | Enables runtime position logging. |

The Mid-360 profiles currently contain `uav5/...` frame names. Adapt those and the sensor calibration to your vehicle. Match `preprocess.lidar_type` to the formats actually handled by the installed FAST-LIO fork, rather than relying only on the comments in an example YAML.

## Visualization

The package includes `rviz.launch.py`, RViz layouts and scripts that adapt visualization settings to `UAV_NAME`. The `tmux/livox_simulation/` session combines the LiDAR simulation with the LUS stack and its own configuration files.

See the [FAST-LIO README](ros_packages/fast_lio/README.md) for estimator details and upstream references.
