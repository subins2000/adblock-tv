<svelte:head>
  <title>ADBTV</title>
</svelte:head>

<main>
  <TopAppBar variant="static" color="primary">
    <Row>
      <Section>
        <IconButton class="material-icons">menu</IconButton>
        <Title>AdBlock TV</Title>
      </Section>
      <Section align="end" toolbar>
        {#if !state.active}
          <IconButton class="material-icons" aria-label="Download" on:click={resume}>play_circle</IconButton>
        {:else}
          <IconButton class="material-icons" aria-label="Download" on:click={pause}>pause_circle</IconButton>
        {/if}
      </Section>
    </Row>
  </TopAppBar>
  <TabBar tabs={['Home', 'Ad-List', 'Settings']} let:tab bind:activeTab>
    <!-- Notice that the `tab` property is required! -->
    <Tab {tab} on:click={() => activeTab = tab}>
      <Label>{tab}</Label>
    </Tab>
  </TabBar>
  <section>
    {#if activeTab === 'Home'}
      <List class="demo-list" dense>
        {#each state.blocks as block}
          <Item>
            <Graphic class="material-icons">stop_circle</Graphic>
            <Text>{block}</Text>
          </Item>
        {/each}
      </List>
    {/if}
    {#if activeTab === 'Ad-List'}
      <div class="mdc-typography--headline6">Add New Advertisement</div><br/>
      <Button on:click={record} variant="raised" disabled={recordDisabled}><Label>Record</Label></Button>
      <Button on:click={recordStop} variant="raised" disabled={stopDisabled}><Label>Stop</Label></Button>
      <br/><br/>
      <div class="mdc-typography--headline6">Ad-List</div><br/>
      <Button on:click={updateIPFS} variant="raised"><Label>Update From IPFS</Label></Button>
      <List class="demo-list" dense>
        {#each state.adlist as adname}
          <Item>
            <Graphic class="material-icons">stop_circle</Graphic>
            <Text>{adname}</Text>
          </Item>
        {/each}
      </List>
    {/if}
    {#if activeTab === 'Settings'}
      <Label>Record duration</Label>
      <Textfield bind:value={state.duration} label="Record duration" type="number" fullwidth /><br/>
      <Label>Confidence</Label>
      <Textfield bind:value={state.confidence} label="Confidence" type="number" fullwidth />
      <br/><br/>
      <Button on:click={saveSettings} variant="raised"><Label>Save</Label></Button>
    {/if}
  </section>
</main>

<script>
  import "@material/typography/mdc-typography.scss";
  import Button from '@smui/button';
  import Textfield, {Input, Textarea} from '@smui/textfield';
  import TopAppBar, {Row, Section, Title} from '@smui/top-app-bar';
  import List, {Group, Item, Graphic, Meta, Separator, Subheader, Text, PrimaryText, SecondaryText} from '@smui/list';
  import Tab, {Icon, Label} from '@smui/tab';
  import TabBar from '@smui/tab-bar';
  import IconButton from '@smui/icon-button';
  
  let state = {
    active: true,
    blocks: [],
    adlist: [],
    duration: 2,
    confidence: 0.15
  }
  let activeTab = "Home"
  let recordDisabled = false
  let stopDisabled = true

  function resume() {
    eel.setState({
      active: true
    })
  }

  function pause() {
    eel.setState({
      active: false
    })
  }

  function updateState(newState) {
    state = newState
  }

  function saveSettings() {
    localStorage['duration'] = state.duration
    localStorage['confidence'] = state.confidence
    eel.updateSettings({
      duration: localStorage['duration'],
      confidence: localStorage['confidence']
    })
  }

  function record() {
    eel.recordStart()
    recordDisabled = true
    stopDisabled = false
  }

  function recordStop() {
    eel.recordStop()
    recordDisabled = false
    stopDisabled = true
    const name = prompt("Ad-name")
    eel.recordFinish(name)
  }

  function updateIPFS() {}

  if (typeof eel !== "undefined") {
    eel.expose(updateState, "updateState");

    if (typeof localStorage['duration'] !== 'undefined') {
      eel.updateSettings({
        duration: localStorage['duration'],
        confidence: localStorage['confidence']
      })
    } else {
      eel.getState()
    }
  }
</script>

<style>
  main {
    margin: -8px;
  }
  section {
    margin: 10px 10px;
  }
</style>