{{- define "devops-guinea-pig.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "devops-guinea-pig.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "devops-guinea-pig.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "devops-guinea-pig.labels" -}}
app.kubernetes.io/name: {{ include "devops-guinea-pig.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "devops-guinea-pig.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{ .Values.serviceAccount.name | default (include "devops-guinea-pig.fullname" .) }}
{{- else -}}
{{ .Values.serviceAccount.name | default "default" }}
{{- end -}}
{{- end -}}