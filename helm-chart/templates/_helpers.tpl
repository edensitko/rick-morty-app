{{/* Return full release name */}}
{{- define "rick-morty-app.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{/* Short name (chart name) */}}
{{- define "rick-morty-app.name" -}}
{{- .Chart.Name -}}
{{- end }}
