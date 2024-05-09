#defining variables
variable "project_id" {
  type    = string
  description = "The Google Cloud project ID."
  default = "metal-appliance-414300"
}

variable "vpc_name" {
  description = "The name of the VPC network"
  type        = list(string)
  default     = ["cloud-vpc12"]
}

variable "zone"{
  description = "The name of the zone"
  type        = string
  default     = "us-west4-b"
}

variable "routing_mode"{
  description = "The type of routing mode"
  type        = string
  default     = "REGIONAL"
}
 
variable "webapp_subnet_cidr" {
  description = "The IP CIDR range for the webapp subnet"
  type        = string
  default     = "10.1.0.0/24"
}

variable "db_subnet_cidr" {
  description = "The IP CIDR range for the db subnet"
  type        = string
  default     = "10.2.0.0/24"
}

variable "machine_type" {
  description = "The machine type"
  type        = string
  default     = "n1-standard-4" 
}

variable "db_disk_type"{
  description = "The disk type"
  type        = string
  default     = "PD-SSD"
}

variable "db_disk_size"{
  description = "The disk size"
  type        = number
  default     = 100
}

variable "custom_image" {
  description = "The custom image for the boot disk of the compute instance"
  type        = string
  default     = "centos-8-image-20240402230039"
}

variable "webapp_reserve_address" {
  description = "The reserve global internal IP address for Private Service Connect "
  type        = string
  default     = "10.0.1.0"
}

variable "region" {
  description = "Region"
  type        =  string
  default     = "us-west4"
}
