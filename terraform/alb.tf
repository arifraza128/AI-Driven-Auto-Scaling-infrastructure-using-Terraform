locals {
  effective_vpc_id = var.vpc_id != null ? var.vpc_id : data.aws_vpc.default[0].id
  subnets_by_az    = { for subnet_id, subnet in data.aws_subnet.by_id : subnet.availability_zone => subnet_id... }
  selected_subnets_by_az = {
    for az, subnet_ids in local.subnets_by_az : az => subnet_ids[0]
    if contains(var.allowed_availability_zones, az)
  }
  effective_subnet_ids = length(var.public_subnet_ids) > 0 ? var.public_subnet_ids : values(local.selected_subnets_by_az)
}

data "aws_vpc" "default" {
  count   = var.vpc_id == null ? 1 : 0
  default = true
}

data "aws_subnets" "default" {
  count = length(var.public_subnet_ids) == 0 ? 1 : 0

  filter {
    name   = "vpc-id"
    values = [local.effective_vpc_id]
  }
}

data "aws_subnet" "by_id" {
  for_each = length(var.public_subnet_ids) == 0 ? toset(data.aws_subnets.default[0].ids) : toset(var.public_subnet_ids)
  id       = each.value
}

resource "aws_lb" "app_lb" {
  name               = "app-lb"
  load_balancer_type = "application"
  subnets            = local.effective_subnet_ids
  security_groups    = [aws_security_group.alb_sg.id]
}

resource "aws_lb_target_group" "app_tg" {
  name     = "app-tg"
  port     = var.app_port
  protocol = "HTTP"
  vpc_id   = local.effective_vpc_id

  health_check {
    path                = "/"
    matcher             = "200"
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 15
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_tg.arn
  }
}
