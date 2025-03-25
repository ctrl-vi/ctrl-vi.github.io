export const prerender = true;

<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>

{@render children()}
