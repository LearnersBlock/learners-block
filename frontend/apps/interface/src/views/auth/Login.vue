<template>
    <el-auth-login
        :title="$t('auth-screen.login.title')"
        :description="$t('auth-screen.login.description')">
    </el-auth-login>
</template>

<script>
import ElAuthLogin from '@/components/Auth/AuthLogin'

export default {
    name: 'Login',
    components: {
        ElAuthLogin
    }
}
</script>
