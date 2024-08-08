CONFIGURATION_SCHEMA = {
    "type": "object",
    "properties": {
        "measurement_unit": {"type": "string"},
        "alert_threshold": {
            "type": "object",
            "properties": {
                "high": {"type": "number"},
                "low": {"type": "number"}
            },
            "required": ["high", "low"]
        },
        "calibration": {
            "type": "object",
            "properties": {
                "offset": {"type": "number"},
                "factor": {"type": "number"}
            },
            "required": ["offset", "factor"]
        }
    },
    "required": ["measurement_unit", "alert_threshold", "calibration"]
}
