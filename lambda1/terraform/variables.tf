variable "GOOGLE_API" {
  type        = string
  default     = ""
  description = "Chave do Google Books APIs"
}

variable "OPENAI_API_KEY" {
  type        = string
  default     = ""
  description = "Chave da OpenAI"
}

variable "STAGE_NAME" {
  type        = string
  default     = "dev"
  description = "O estágio atual de deploy da API (dev ou prod)."
}
