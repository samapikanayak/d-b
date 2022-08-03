variable "access_key" {
  description = "Name to be used on all the resources as identifier"
  type        = string
  default     = ""
}

variable "secret_key" {
  description = "Name to be used on all the resources as identifier"
  type        = string
  default     = ""
}
variable "single_nat_gateway" {
  description = "Name to be used on all the resources as identifier"
  type        = string
  default     = "true"
}

variable "name" {
  description = "Name to be used on all the resources as identifier"
  type        = string
  default     = ""
}

variable "cidr" {
  description = "The CIDR block for the VPC. Default value is a valid CIDR, but not acceptable by AWS and should be overridden"
  type        = string
  default     = "10.1.0.0/16"
}

variable "public_subnets" {
  description = "A list of public subnets inside the VPC"
  type        = list(string)
  default     = ["10.1.3.0/24", "10.1.4.0/24"]
}

variable "private_subnets" {
  description = "A list of private subnets inside the VPC"
  type        = list(string)
  default     = ["10.1.5.0/24", "10.1.6.0/24"]
}
variable "azs" {
  description = "A list of private subnets inside the VPC"
  type        = list(string)
  default     = ["us-east-2a", "us-east-2b"]
}


variable "namespace" {
  default     = "devstaging"
  description = "The environment prefix name given to create lable for the resources from label module "
}

variable "region" {
  description = "AWS Region"
  default     = "us-east-2"
}

variable "profile" {
  description = "AWS Profile"
  default     = "default"
}
variable "tenant" {
  default     = "dbsupply"
  description = "The app/organization name given to create lable for the resources from label module "
}
variable "navsoftip" {
  default     = "111.93.177.10/32"
  description = "Office IP of Navsoft"
}


variable "sonarqube" {
  default     = "3.214.23.165/32"
  description = "Sonarqube IP of Navsoft"
}


variable "instance_class" {
  default = "db.m6g.large"
  description = "The instance type of the RDS instance"
  type        = string
}

variable "username" {
  default = "dnbsupply_usr"
  description = "Username for the master DB user"
  type        = string
}

variable "password" {
  default = "5%Eqtuez790i"
  description = "Password for the master DB user. Note that this may show up in logs, and it will be stored in the state file"
  type        = string
}

variable "s3bucketname" {
  default = ""
  description = "S3 Bucket Name"
  type        = string
}