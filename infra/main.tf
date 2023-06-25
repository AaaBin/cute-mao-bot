terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file("cute-mao-plurk-bot-4c3d700da585.json")

  project = "cute-mao-plurk-bot"
  region  = "us-central1"
  zone    = "us-central1-c"
}

resource "google_cloud_run_v2_job" "default" {
  client       = "cloud-console"
  labels       = {}
  launch_stage = "GA"
  location     = "us-central1"
  name         = "mao-bot"
  project      = "cute-mao-plurk-bot"

  template {
    labels      = {}
    parallelism = 0
    task_count  = 1

    template {
      execution_environment = "EXECUTION_ENVIRONMENT_GEN2"
      max_retries           = 0
      service_account       = "245906654942-compute@developer.gserviceaccount.com"
      timeout               = "60s"

      containers {
        args    = []
        command = []
        image   = "birnie1571/mao-bot:latest"

        env {
          name  = "EXECUTE_GAP"
          value = "15"
        }
        env {
          name = "TOKEN_KEY"

          value_source {
            secret_key_ref {
              secret  = "TOKEN_KEY"
              version = "1"
            }
          }
        }
        env {
          name = "API_KEY"

          value_source {
            secret_key_ref {
              secret  = "API_KEY"
              version = "1"
            }
          }
        }
        env {
          name = "API_SECRET"

          value_source {
            secret_key_ref {
              secret  = "API_SECRET"
              version = "1"
            }
          }
        }
        env {
          name = "TOKEN_SECRET"

          value_source {
            secret_key_ref {
              secret  = "TOKEN_SECRET"
              version = "1"
            }
          }
        }

        resources {
          limits = {
            "cpu"    = "1000m"
            "memory" = "512Mi"
          }
        }
      }
    }
  }

  timeouts {}
}
