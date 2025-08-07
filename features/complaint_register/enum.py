from enum import Enum


class ComplaintCategory(str, Enum):
    WATER_SUPPLY = "Water Supply Issues"
    ELECTRICITY = "Electricity Problems"
    ROAD_INFRASTRUCTURE = "Road & Infrastructure"
    WASTE_MANAGEMENT = "Waste Management"
    DRAINAGE_SEWAGE = "Drainage & Sewage"
    PUBLIC_SAFETY = "Public Safety"
    TRANSPORT_TRAFFIC = "Transport & Traffic"
    HEALTH_SANITATION = "Health & Sanitation"
    POLLUTION = "Pollution"
    UNAUTHORIZED_CONSTRUCTION = "Unauthorized Construction & Encroachment"
