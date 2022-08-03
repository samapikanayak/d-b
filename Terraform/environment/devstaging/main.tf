#####################
## VPC
#####################

module "vpc_label" {
  source = "../../module/terraform-null-label"

  tenant      = var.tenant
  namespace   = var.namespace
  name        = "vpc"
  delimiter   = "-"
  label_order = ["tenant", "namespace", "stage", "name", "attributes"]

  additional_tag_map = {
    ManagedBy = "Terraform"
  }
}

module "vpc" {
  source = "../../module/vpc/"

  name            = module.vpc_label.id
  cidr            = var.cidr
  azs             = var.azs
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets

  enable_dns_hostnames       = true
  enable_dns_support         = true
  enable_nat_gateway         = true
  single_nat_gateway         = true
  manage_default_route_table = true
  default_route_table_tags   = { DefaultRouteTable = true }

  manage_default_security_group  = true
  default_security_group_ingress = []
  default_security_group_egress = [
    {
      protocol         = "-1"
      from_port        = 0
      to_port          = 0
      cidr_blocks      = "0.0.0.0/0"
      ipv6_cidr_blocks = "::/0"
    }
  ]

  tags = {
    Terraform = "true"
    Environment = "dev"
  }

}

module "https_label" {
  source = "../../module/terraform-null-label"

  tenant      = var.tenant
  namespace   = var.namespace
  name        = "https"
  delimiter   = "-"
  label_order = ["tenant", "namespace", "stage", "name", "attributes"]

  additional_tag_map = {
    ManagedBy = "Terraform"
  }
}

module "https-security_group" {
  source = "../../module/terraform-aws-security-group"
  name            = "security group https"
  use_name_prefix = false
  description     = "Security group for Navsoft EC2 instance"
  vpc_id          = module.vpc.vpc_id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["http-80-tcp", "https-443-tcp"]
  egress_rules        = ["all-all"]

  tags = module.vpc_label.additional_tag_map
}


###################
### RDS-postgresql
###################

module "rds_label" {
  source = "../../module/terraform-null-label"

  tenant      = var.tenant
  namespace   = var.namespace
  name        = "postgres-rds"
  delimiter   = "-"
  label_order = ["tenant", "namespace", "stage", "name", "attributes"]

  additional_tag_map = {
    ManagedBy = "Terraform"
  }
}

module "rds_security_group" {
  source = "../../module/terraform-aws-security-group"

  name        = module.rds_label.id
  description = "Postgres RDS Security Group"
  vpc_id      = module.vpc.vpc_id

  # ingress
  ingress_with_cidr_blocks = [
    {
      from_port   = 5432
      to_port     = 5432
      protocol    = "tcp"
      description = "PostgreSQL access from within VPC"
      cidr_blocks = module.vpc.vpc_cidr_block
    },
    {
      from_port   = 5432
      to_port     = 5432
      protocol    = "tcp"
      description = "PostgreSQL access from Navsoft"
      cidr_blocks = var.navsoftip
    }
  ]

  tags = module.rds_label.additional_tag_map
}

module "rds_external_label" {
  source = "../../module/terraform-null-label"

  tenant      = var.tenant
  namespace   = var.namespace
  name        = "postgres-rds-public"
  delimiter   = "-"
  label_order = ["tenant", "namespace", "stage", "name", "attributes"]

  additional_tag_map = {
    ManagedBy = "Terraform"
  }
}

module "rds_public_access_sg" {
  source = "../../module/terraform-aws-security-group"

  name        = module.rds_external_label.id
  description = "Postgres RDS Public Access Security Group"
  vpc_id      = module.vpc.vpc_id

  # ingress
  ingress_with_cidr_blocks = [
    {
      from_port   = 5432
      to_port     = 5432
      protocol    = "tcp"
      description = "PostgreSQL access from Navsoft us-east-1"
      cidr_blocks = var.navsoftip
    },
  ]

  tags = module.rds_external_label.additional_tag_map
}

module "db" {
  source = "../../module/terraform-aws-rds"

  identifier                            = module.rds_label.id
  engine                                = "postgres"
  engine_version                        = "14.2"
  family                                = "postgres14"
  major_engine_version                  = "14"
  instance_class                        = var.instance_class
  allocated_storage                     = 100
  max_allocated_storage                 = 200
  storage_encrypted                     = true
  username                              = var.username
  password                              = var.password
  port                                  = 5432
  multi_az                              = false
  subnet_ids                            = module.vpc.public_subnets
  vpc_security_group_ids                = [module.rds_security_group.security_group_id, module.rds_public_access_sg.security_group_id]
  publicly_accessible                   = true
  maintenance_window                    = "Mon:00:00-Mon:03:00"
  backup_window                         = "03:00-06:00"
  enabled_cloudwatch_logs_exports       = ["postgresql", "upgrade"]
  backup_retention_period               = 7
  skip_final_snapshot                   = true
  deletion_protection                   = true
  performance_insights_enabled          = true
  performance_insights_retention_period = 7
  create_monitoring_role                = true
  monitoring_interval                   = 60
  monitoring_role_name                  = "${module.rds_label.id}-role"
  monitoring_role_description           = "RDS monitoring role"
  apply_immediately                     = true

  tags = module.rds_label.additional_tag_map
}

##############
## S3 Buckets
##############

module "s3_bucket" {
  source = "../../module/terraform-aws-s3-bucket"

  acl                = "private"
  enabled            = true
  versioning_enabled = true
  label_order        = ["tenant", "namespace", "stage", "name", "attributes"]
  name               = var.s3bucketname
  tenant             = var.tenant
  namespace          = "dev"
}

module "cloudtrail" {
  source                        = "../../module/terraform-aws-cloudtrail"
  name                          = "dbsupply-cloudtrail"
  enable_logging                = true
  enable_log_file_validation    = false
  include_global_service_events = false
  is_multi_region_trail         = false
  is_organization_trail         = false
  s3_bucket_name                = module.cloudtrail_s3_bucket.bucket_id
}

module "cloudtrail_s3_bucket" {
  source        = "../../module/terraform-aws-cloudtrail-s3-bucket"
  label_order   = ["tenant", "namespace", "stage", "name"]
  tenant        = var.tenant
  name          = "cloudtrail"
  namespace     = var.namespace
  force_destroy = true
}

###################
## ES dev EC2
###################




module "dev_es_label" {
  source = "../../module/terraform-null-label"

  tenant      = var.tenant
  namespace   = var.namespace
  name        = "es-dev"
  delimiter   = "-"
  label_order = ["tenant", "namespace", "stage", "name", "attributes"]

  additional_tag_map = {
    ManagedBy = "Terraform"
  }
}

module "dev-es-security_group" {
  source = "../../module/terraform-aws-security-group"

  name            = module.dev_es_label.id
  use_name_prefix = false
  description     = "Security group for bastion EC2 instance"
  vpc_id          = module.vpc.vpc_id

  ingress_cidr_blocks = []
  ingress_rules       = []
  egress_rules        = ["all-all"]

  ingress_with_self = [
    {
      from_port   = 9200
      to_port     = 9200
      protocol    = "tcp"
      description = "ES Nodes Communication"
      self        = true
    },
    {
      from_port   = 9300
      to_port     = 9300
      protocol    = "tcp"
      description = "ES Nodes Communication"
      self        = true
    },
  ]

  ingress_with_source_security_group_id = [
    {
      from_port                = 80
      to_port                  = 80
      protocol                 = "tcp"
      description              = "ES access from Public"
      source_security_group_id = module.https-security_group.security_group_id
    },
    {
      from_port                = 443
      to_port                  = 443
      protocol                 = "tcp"
      description              = "SSH access from Public"
      source_security_group_id = module.https-security_group.security_group_id
    }
  ]

  ingress_with_cidr_blocks = [
    {
      from_port   = 9200
      to_port     = 9200
      protocol    = "tcp"
      description = "ES Access within VPC"
      cidr_blocks = module.vpc.vpc_cidr_block
    },
    {
      from_port   = 0
      to_port     = 65500
      protocol    = "tcp"
      description = "Navsoft Access"
      cidr_blocks =  var.navsoftip
    },
   {
      from_port   = 0
      to_port     = 65500
      protocol    = "tcp"
      description = "Navsoft sonarqube"
      cidr_blocks =  var.sonarqube
   } 


  ]

  tags = module.dev_es_label.additional_tag_map
}

module "dev_es_ssh_key_pair" {
  source = "../../module/terraform-aws-key-pair"

  namespace             = var.namespace
  tenant                = var.tenant
  name                  = "dev-es"
  label_order           = ["tenant", "namespace", "stage", "name", "attributes"]
  ssh_public_key_path   = "./secrets"
  generate_ssh_key      = "true"
  private_key_extension = ".pem"
  public_key_extension  = ".pub"
}

module "dev-es-ec2-1" {
  source = "../../module/terraform-aws-ec2-instance"

  name                        = "${module.dev_es_label.id}-master"
  key_name                    = module.dev_es_ssh_key_pair.key_name
  ami                         = "ami-0629230e074c580f2"
  instance_type               = "t3.xlarge"
  availability_zone           = element(module.vpc.azs, 0)
  subnet_id                   = element(module.vpc.public_subnets, 0)
  vpc_security_group_ids      = [module.dev-es-security_group.security_group_id]
  associate_public_ip_address = true
  tags = module.dev_es_label.additional_tag_map
  user_data = <<-EOF
      #!/bin/sh
      sudo apt-get update
      sudo apt install openjdk-11-jdk
      wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
      sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
      sudo apt update
      sudo apt install jenkins
      sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent 
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
      sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" 
      sudo apt-get update
      sudo apt-get install docker-ce docker-ce-cli containerd.i
      software-properties-common
      sudo gpasswd -a jenkins docker
      EOF 
}

resource "aws_eip" "dev-es-ec2-1" {
  instance = module.dev-es-ec2-1.id
  vpc      = true

  tags = module.dev_es_label.additional_tag_map

}

resource "aws_volume_attachment" "dev-es-ec2-1" {
  device_name = "/dev/sdh"
  volume_id   = aws_ebs_volume.dev-es-ec2-1.id
  instance_id = module.dev-es-ec2-1.id
}

resource "aws_ebs_volume" "dev-es-ec2-1" {
  availability_zone = element(module.vpc.azs, 0)
  size              = 50
}

module "dev-es-ec2-2" {
  source = "../../module/terraform-aws-ec2-instance"

  name                        = module.dev_es_label.id
  key_name                    = module.dev_es_ssh_key_pair.key_name
  ami                         = "ami-0629230e074c580f2"
  instance_type               = "t3.xlarge"
  availability_zone           = element(module.vpc.azs, 1)
  subnet_id                   = element(module.vpc.public_subnets, 1)
  vpc_security_group_ids      = [module.dev-es-security_group.security_group_id]
  associate_public_ip_address = true
  user_data = <<-EOF
      #!/bin/sh
      sudo apt-get update
      sudo apt install openjdk-11-jdk
      wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
      sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
      sudo apt update
      sudo apt install jenkins
      sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent 
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
      sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" 
      sudo apt-get update
      sudo apt-get install docker-ce docker-ce-cli containerd.i
      software-properties-common
      sudo gpasswd -a jenkins docker
      EOF
  tags = module.dev_es_label.additional_tag_map
}

resource "aws_eip" "dev-es-ec2-2" {
  instance = module.dev-es-ec2-2.id
  vpc      = true

  tags = module.dev_es_label.additional_tag_map
}

resource "aws_volume_attachment" "dev-es-ec2-2" {
  device_name = "/dev/sdh"
  volume_id   = aws_ebs_volume.dev-es-ec2-2.id
  instance_id = module.dev-es-ec2-2.id
}

resource "aws_ebs_volume" "dev-es-ec2-2" {
  availability_zone = element(module.vpc.azs, 1)
  size              = 50
}
/*
#################
## SSM Parameter
#################

module "ssm_label" {
  source = "../../module/terraform-null-label"

  tenant      = var.tenant
  namespace   = "dev"
  name        = ""
  delimiter   = "-"
  label_order = ["tenant", "namespace", "stage", "name"]
}


module "ssm-parameter" {
  source = "../../module/terraform-aws-ssm-parameter-store"


  parameter_write = [
    {
      name        = "${module.ssm_label.id}-DB_SERVICE"
      value       = module.db.db_instance_address
      type        = "SecureString"
      kms_arn     = data.aws_kms_alias.ssm.arn
      overwrite   = "true"
      description = "RDS Endpoint"
    }
      ]

  tags = {
    ManagedBy = "Terraform"
  }


}
###################
## CW ALARM Label
###################

module "cw_label" {
  source = "../../module/terraform-null-label"

  tenant      = var.tenant
  namespace   = var.namespace
  name        = ""
  delimiter   = "-"
  label_order = ["tenant", "namespace", "stage", "name"]
}

####################
## RDS Alarms
####################

module "cw-alarm-RDS-High_CPU" {

  source = "../../module/cloudwatch-alarms"

  region                    = var.region
  alarm_name                = "${module.cw_label.id}-RDS-High_CPU"
  alarm_description         = "RDS CPU above 70"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "1"
  metric_name               = "CPUUtilization"
  namespace                 = "AWS/RDS"
  period                    = "300"
  statistic                 = "Average"
  threshold                 = "70.0"
  treat_missing_data        = "breaching"
  alarm_actions             = [module.sns_alerts.sns_topic_arn]
  ok_actions                = [module.sns_alerts.sns_topic_arn]
  insufficient_data_actions = [module.sns_alerts.sns_topic_arn]

  dimensions = {
    DBInstanceIdentifier = module.rds_label.id
  }
}

module "cw-alarm-RDS-Low_Storage_Space" {

  source                    = "../../module/cloudwatch-alarms"
  region                    = var.region
  alarm_name                = "${module.cw_label.id}-RDS-Low_Storage_Space"
  alarm_description         = "RDS Low Storage Space < 20GB"
  comparison_operator       = "LessThanOrEqualToThreshold"
  evaluation_periods        = "1"
  metric_name               = "FreeStorageSpace"
  namespace                 = "AWS/RDS"
  period                    = "60"
  statistic                 = "Minimum"
  threshold                 = "30000000000.0"
  treat_missing_data        = "breaching"
  alarm_actions             = [module.sns_alerts.sns_topic_arn]
  ok_actions                = [module.sns_alerts.sns_topic_arn]
  insufficient_data_actions = [module.sns_alerts.sns_topic_arn]

  dimensions = {
    DBInstanceIdentifier = module.rds_label.id
  }
}

resource "aws_db_event_subscription" "rds_events" {
  name      = "${module.cw_label.id}-RDS-Events"
  sns_topic = module.sns_alerts.sns_topic_arn

  source_type = "db-instance"
  source_ids  = [module.db.db_instance_id]

  event_categories = [
    "availability",
    "deletion",
    "failover",
    "failure",
    "low storage",
    "maintenance",
    "notification",
    "read replica",
    "recovery",
    "restoration",
  ]
}

####################
## ES EC2 Alarms
####################

module "cw-alarm-ES-Dev-Master-High_CPU" {

  source                    = "../../module/cloudwatch-alarms"
  region                    = var.region
  alarm_name                = "${module.cw_label.id}-ES-Dev-Master-High_CPU"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  metric_name               = "CPUUtilization"
  namespace                 = "AWS/EC2"
  period                    = "120"
  statistic                 = "Average"
  threshold                 = "70"
  treat_missing_data        = "breaching"
  alarm_description         = "ES Dev Master CPU above 70"
  alarm_actions             = [module.sns_alerts.sns_topic_arn]
  ok_actions                = [module.sns_alerts.sns_topic_arn]
  insufficient_data_actions = [module.sns_alerts.sns_topic_arn]

  dimensions = {
    InstanceId = module.dev-es-ec2-1.id
  }
}

module "cw-alarm-ES-Dev-Master-Status_Check_Fail" {
  source = "../../module/cloudwatch-alarms"

  region                    = var.region
  alarm_name                = "${module.cw_label.id}-ES-Dev-Master-Status_Check_Fail"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  metric_name               = "StatusCheckFailed"
  namespace                 = "AWS/EC2"
  period                    = "60"
  statistic                 = "Maximum"
  threshold                 = "1.0"
  treat_missing_data        = "breaching"
  alarm_description         = "ES Dev Master Status Check Fail"
  alarm_actions             = [module.sns_alerts.sns_topic_arn]
  ok_actions                = [module.sns_alerts.sns_topic_arn]
  insufficient_data_actions = [module.sns_alerts.sns_topic_arn]

  dimensions = {
    InstanceId = module.dev-es-ec2-1.id
  }
}

module "cw-alarm-ES-Dev-Node-2-High_CPU" {

  source                    = "../../module/cloudwatch-alarms"
  region                    = var.region
  alarm_name                = "${module.cw_label.id}-ES-Dev-Node-2-High_CPU"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  metric_name               = "CPUUtilization"
  namespace                 = "AWS/EC2"
  period                    = "120"
  statistic                 = "Average"
  threshold                 = "70"
  treat_missing_data        = "breaching"
  alarm_description         = "ES Dev Node-2 CPU above 70"
  alarm_actions             = [module.sns_alerts.sns_topic_arn]
  ok_actions                = [module.sns_alerts.sns_topic_arn]
  insufficient_data_actions = [module.sns_alerts.sns_topic_arn]

  dimensions = {
    InstanceId = module.dev-es-ec2-2.id
  }
}

module "cw-alarm-ES-Dev-Node-2-Status_Check_Fail" {
  source = "../../module/cloudwatch-alarms"

  region                    = var.region
  alarm_name                = "${module.cw_label.id}-ES-Dev-Node-2-Status_Check_Fail"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  metric_name               = "StatusCheckFailed"
  namespace                 = "AWS/EC2"
  period                    = "60"
  statistic                 = "Maximum"
  threshold                 = "1.0"
  treat_missing_data        = "breaching"
  alarm_description         = "ES Dev Node-2 Status Check Fail"
  alarm_actions             = [module.sns_alerts.sns_topic_arn]
  ok_actions                = [module.sns_alerts.sns_topic_arn]
  insufficient_data_actions = [module.sns_alerts.sns_topic_arn]

  dimensions = {
    InstanceId = module.dev-es-ec2-2.id
  }
}
*/