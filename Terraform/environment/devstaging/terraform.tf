//Specifying provider/terraform version
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.63"
    }
  }

  required_version = "~> 1.0"
}

//provider "AWS"
provider "aws" {
  region  = var.region
  access_key = var.access_key
  secret_key = var.secret_key
}

# N. virginia region to create the Amazon certificate
# provider "aws" {
#   region  = "us-east-1"
#   alias   = "acm-virginia"
#   profile = var.profile
# }

##############################################################################################

//Using s3 bucket as remote state management
//terraform init

terraform {
  backend "s3" {
    encrypt        = true
    bucket         = "dbsupply-backend-tfstate"
    key            = "state.tfstate"
    region         = "us-east-2"
    dynamodb_table = "dbsupply-tfstate-lock"
  }
}