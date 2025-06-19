# The Think Tank

The Think Tank is an open source robotics project that brings together control algorithms, vision systems, hardware configuration and a mobile app. This repository is a central place for all the components that power the platform.

## Repository layout

- **control/** – robot control logic. Includes `motion` for drive control and `turret` for managing the firing mechanism.
- **hardware/** – configuration files and documentation for the physical build.
- **interface/** – networking layers. The `api` folder hosts the HTTP API while `websocket` contains the real‑time socket server.
- **ios-app/** – source for the companion iOS application.
- **tests/** – test suites and supporting assets.
- **utils/** – shared utilities used across the codebase.
- **vision/** – computer vision code. Contains `model` for machine learning models and `streaming` for video pipelines.

See the README files in each folder for more details as development progresses.
